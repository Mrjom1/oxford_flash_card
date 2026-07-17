import json
import requests
import re
import time
import os
from collections import defaultdict

# ==========================================
# ⚙️ ตั้งค่าการใช้งาน
# ==========================================
USE_API = False  # True = ใช้ Gemini API, False = ใช้ Ollama (default = Ollama ตามที่ตกลงกัน)

# 1. ตั้งค่าสำหรับ Ollama
OLLAMA_MODEL = "qwen3:8b"
OLLAMA_THINK = False  # ปิด thinking mode เพื่อความเร็ว — ยอมรับผลจากรอบทดสอบแล้ว (~30-45s/คำ)

# 2. ตั้งค่าสำหรับ Gemini API (สำรองไว้เผื่ออยากสลับกลับ)
GEMINI_API_KEY = "ใส่_API_KEY_ของคุณที่นี่"

SAVE_EVERY_N = 10  # autosave ทุกๆ N คำ — นับรวมทั้งไฟล์ ไม่ใช่แยกราย JLPT level
# ==========================================

if USE_API:
    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY)

# JSON schema บังคับ output ให้ตรง format เสมอ
# ex_th: คำแปลไทยของประโยคตัวอย่าง — ช่วยตรวจสอบได้แม้ไม่รู้ภาษาญี่ปุ่น และเป็น cross-check เพิ่มอีกชั้น
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "m_en": {"type": "string"},
        "m_th": {"type": "string"},
        "ex": {"type": "array", "items": {"type": "string"}},
        "ex_th": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["m_en", "m_th", "ex", "ex_th"],
}


def build_prompt(word, kana, current_m_en, current_m_th):
    # ผ่านการทดสอบเทียบ 4 โมเดล + ปรับแก้ 2 รอบแล้ว (เลือก qwen3:8b, แก้บั๊กฮิรางานะ, เพิ่ม ex_th)
    return f"""
You are an expert Japanese-Thai dictionary creator and JLPT instructor.
Enhance and fix the following Japanese vocabulary entry.
Word (Kanji/Kana): {word}
Reading (kana): {kana}
POS:
Current English Meaning: {current_m_en}
Current Thai Meaning: {current_m_th}

Instructions:
1. Provide a short, accurate English meaning (m_en).
2. Provide a natural, accurate Thai meaning (m_th).
3. Generate ONE natural Japanese example sentence using this word. CRITICAL rules for this sentence:
   (a) This word may have multiple readings with different meanings, or multiple kanji sharing the same reading — the sentence MUST use the exact word and reading "{word}" / "{kana}" given above. Do NOT substitute a different reading of the same kanji, and do NOT substitute a different (even homophonous) kanji.
   (b) Write the word using its standard, normal orthography exactly as shown in "Word (Kanji/Kana)" above. If it is normally written in kanji, use kanji — do NOT spell it out phonetically in hiragana instead. Only use hiragana/katakana if that is genuinely how the word is normally written.
   (c) Suitable for its JLPT level.
4. Provide a natural Thai translation of that EXACT example sentence in 'ex_th' (translate the sentence itself, not just repeat m_th).
5. 'ex' and 'ex_th' must each contain EXACTLY ONE string. 'ex' must be written ENTIRELY in Japanese (no Thai/English/Chinese/romanization mixed in). 'ex_th' must be written ENTIRELY in Thai (no Japanese/English romanization mixed in).
6. Output ONLY a valid JSON object without markdown formatting.

Format:
{{"m_en": "...", "m_th": "...", "ex": ["...ประโยคภาษาญี่ปุ่นล้วนเท่านั้น..."], "ex_th": ["...คำแปลไทยของประโยคนั้นล้วนเท่านั้น..."]}}
"""


def get_fixed_data(word, kana, current_m_en, current_m_th):
    prompt = build_prompt(word, kana, current_m_en, current_m_th)
    result = None

    if USE_API:
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                result = response.text
                time.sleep(5)  # พัก 5 วินาที
                break
            except Exception as e:
                error_msg = str(e)
                # ดักจับ Error ส่งถี่เกินไป (429) และ เซิร์ฟเวอร์เต็ม (503)
                if "429" in error_msg or "quota" in error_msg.lower() or "503" in error_msg:
                    print(f" [เซิร์ฟเวอร์ Google โหลดหนัก ขอพัก 20 วินาที...] ", end="", flush=True)
                    time.sleep(20)
                else:
                    print(f"\n[!] Gemini API Error: {e}")
                    return None
        else:
            return None

    else:
        # ส่วนของ Ollama
        try:
            res = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "think": OLLAMA_THINK,
                    "format": RESPONSE_SCHEMA,
                }
            )

            if res.status_code != 200:
                print(f"\n[!] Ollama Server Error: {res.text}")
                return None

            result = res.json().get('response', '')

            if not result.strip():
                print(f"\n[!] Error: Ollama returned an empty response.")
                return None

        except requests.exceptions.ConnectionError:
            print("\n[!] Connection Error: Ollama is not running. Please start it first.")
            return None
        except Exception as e:
            print(f"\n[!] Unexpected Error: {e}")
            return None

    # --- ส่วน parse JSON (ใช้ร่วมกันทั้งสองเส้นทาง) ---
    # เช็คก่อนว่า result ไม่ใช่ None/ว่างเปล่า กัน crash ทั้งสคริปต์ถ้า response.text
    # ของ Gemini ออกมาเป็น None (เช่นโดน safety filter บล็อก)
    if not result or not str(result).strip():
        print(f"\n[!] Empty/blank model output for word '{word}'.")
        return None

    try:
        clean_result = re.sub(r'```json|```', '', result).strip()
        match = re.search(r'\{.*\}', clean_result, re.DOTALL)
        if match:
            clean_result = match.group(0)

        parsed_json = json.loads(clean_result)

        if not isinstance(parsed_json, dict):
            print(f"\n[!] Unexpected JSON shape (not an object) for word '{word}'.")
            return None

        return parsed_json
    except (json.JSONDecodeError, TypeError) as e:
        print(f"\n[!] JSON Parse Error for word '{word}': {e}. Raw output:\n{result}")
        return None


def save_progress(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def flag_homographs(data, flag_file):
    """สแกนหาคำที่ 'w' ซ้ำกัน (หลายคำอ่าน/ความหมายในคันจิเดียวกัน) แล้วบันทึกแยกไว้ต่างหาก
    เหตุผล: จากรอบทดสอบ 46 entries พบว่าโมเดลแยกความหมายคำพ้องรูปได้ไม่สมบูรณ์
    (4/7 คู่ที่ทดสอบ ได้ประโยคตัวอย่างซ้ำกันเป๊ะทั้งที่ควรต่างกัน) จึงบันทึกรายชื่อไว้ให้ตรวจสอบเพิ่มเติมทีหลัง
    แทนที่จะพยายามแก้ปัญหานี้ด้วย prompt ให้สมบูรณ์ 100% ซึ่งไม่น่าเป็นไปได้จริงกับโมเดลขนาดนี้"""
    word_groups = defaultdict(list)
    for level, words_list in data.items():
        if not isinstance(words_list, list):
            continue
        for item in words_list:
            word_groups[item.get('w')].append({
                "level": level,
                "kana": item.get('kana'),
                "m_en": item.get('m_en'),
            })

    homographs = {w: entries for w, entries in word_groups.items() if len(entries) > 1}

    with open(flag_file, 'w', encoding='utf-8') as f:
        json.dump(homographs, f, ensure_ascii=False, indent=2)

    total_entries = sum(len(v) for v in homographs.values())
    print(f"🔍 พบคำพ้องรูป {len(homographs)} คำ ({total_entries} entries) — บันทึกรายชื่อไว้ที่ '{flag_file}' เพื่อตรวจสอบทีหลัง")
    print("   (จากรอบทดสอบ: โมเดลแยกความหมายคำพ้องรูปได้ไม่สมบูรณ์ ~4/7 คู่ทดสอบได้ประโยคตัวอย่างซ้ำกัน)\n")


def main():
    print(f"⏳ Loading Japanese JSON file (USE_API = {USE_API})...")

    input_file = 'words_jp.json'
    output_file = 'words_jp_fixed.json'
    homograph_flag_file = 'words_jp_homographs_review.json'

    # 🌟 เช็คว่ามีไฟล์เก่าที่ทำค้างไว้ไหม จะได้ทำต่อเลย
    if os.path.exists(output_file):
        print(f"📂 Found existing progress in '{output_file}', resuming from there...")
        load_file = output_file
    else:
        load_file = input_file

    try:
        with open(load_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[!] Error: Could not find '{load_file}' in this folder.")
        return

    # สแกนหาคำพ้องรูปไว้ตรวจทีหลัง — ทำครั้งเดียวตอนเริ่ม ไม่ต้องรอจนรันครบ
    flag_homographs(data, homograph_flag_file)

    # นับ global ทั้งไฟล์ ไม่ใช่แยกราย level (กันบั๊ก level เล็กไม่เคย trigger autosave)
    processed_since_save = 0

    try:
        for level, words_list in data.items():
            if not isinstance(words_list, list):
                continue

            print(f"\n--- Processing JLPT Level: {level} ---")
            for i, item in enumerate(words_list):
                word = item.get('w')
                kana = item.get('kana', '')
                m_en = item.get('m_en', '')
                m_th = item.get('m_th', '')

                # 🌟 ถ้ามีป้าย is_fixed แปลว่าทำเสร็จแล้ว ให้ข้ามไปเลย
                if item.get('is_fixed') == True:
                    continue

                timestamp = time.strftime('%H:%M:%S')
                print(f"[{timestamp}] [{i+1}/{len(words_list)}] Fixing: '{word}' ({kana}) ... ", end="", flush=True)

                start_time = time.time()
                fixed_data = get_fixed_data(word, kana, m_en, m_th)
                elapsed = time.time() - start_time

                if fixed_data:
                    item['m_en'] = fixed_data.get('m_en', m_en)
                    item['m_th'] = fixed_data.get('m_th', m_th)
                    item['ex'] = fixed_data.get('ex', item.get('ex', []))
                    item['ex_th'] = fixed_data.get('ex_th', item.get('ex_th', []))
                    item['is_fixed'] = True  # แปะป้ายว่าคำนี้แก้ไขเสร็จเรียบร้อยแล้ว
                    print(f"Done -> {item['m_th']} (⏱️ {elapsed:.1f}s)")
                else:
                    print(f"Failed (Skipped for now) (⏱️ {elapsed:.1f}s)")

                processed_since_save += 1
                if processed_since_save >= SAVE_EVERY_N:
                    save_progress(data, output_file)
                    processed_since_save = 0

    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user (Ctrl+C). Saving progress before exiting...")
    finally:
        # save เสมอไม่ว่าจะจบงานปกติ, ถูก Ctrl+C, หรือ error ที่ไม่คาดคิดเกิดขึ้นกลางทาง
        save_progress(data, output_file)
        print(f"\n🎉 Progress saved to '{output_file}'")


if __name__ == "__main__":
    main()
