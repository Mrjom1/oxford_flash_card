import json
import requests
import re
import time
import os

# ==========================================
# ⚙️ ตั้งค่าการใช้งาน
# ==========================================
USE_API = False  # True = ใช้ Gemini API, False = ใช้ Ollama (default = Ollama ตามที่ตกลงกัน)

# 1. ตั้งค่าสำหรับ Ollama
OLLAMA_MODEL = "qwen3:8b"
OLLAMA_THINK = False  # Qwen3 เปิด thinking mode เป็นค่าเริ่มต้นบน Ollama ซึ่งเพิ่ม latency
                       # มากสำหรับงาน short lookup แบบนี้ ปิดไว้เพื่อความเร็ว (ทดสอบแล้วได้ ~14-19s/คำ)

# 2. ตั้งค่าสำหรับ Gemini API
GEMINI_API_KEY = "ใส่_API_KEY_ของคุณที่นี่"  # 🛑 อย่าลืมใส่ API Key นะครับ

SAVE_EVERY_N = 10  # autosave ทุกๆ N คำ — นับรวมทั้งไฟล์ ไม่ใช่แยกราย CEFR level
# ==========================================

if USE_API:
    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY)

# JSON schema สำหรับบังคับให้ Ollama ตอบเป็น JSON ตรงตาม structure นี้เสมอ
# (ลดการพึ่งพา regex แกะ markdown code fence ออกจาก free-form text)
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "m_en": {"type": "string"},
        "m_th": {"type": "string"},
    },
    "required": ["m_en", "m_th"],
}


def get_fixed_data(word, pos, current_m_en):
    prompt = f"""
You are an expert English-Thai dictionary creator.
Fix the following vocabulary entry.
Word: {word}
POS: {pos}
Current English Meaning: {current_m_en}
Instructions:
1. If the "Current English Meaning" contains "API Error", garbage text, or is blank, write a short, accurate English definition based on the Word and POS. Otherwise, keep it as is or improve it slightly.
2. Provide a VERY SHORT and accurate English definition based on the Word and POS (Maximum 5-10 words).
3. Provide a VERY SHORT and precise Thai meaning (m_th). Give ONLY 1-3 direct translated words or synonyms (e.g. "สวย, งดงาม"). DO NOT write any explanations or sentences in the Thai meaning.
4. Output ONLY a valid JSON object without markdown formatting.
Format:
{{"m_en": "...", "m_th": "..."}}
"""

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
    # ของ Gemini ออกมาเป็น None (เช่นโดน safety filter บล็อก) ซึ่ง re.sub() จะ throw
    # TypeError ถ้าไม่เช็คก่อน
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


def main():
    print(f"⏳ Loading JSON file (USE_API = {USE_API})...")

    input_file = 'words_en.json'
    output_file = 'words_en_fixed.json'

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

    # นับ global ทั้งไฟล์ — เวอร์ชันเดิมนับแยกราย level (ตัวแปร i รีเซ็ตทุก level)
    # ทำให้ level ที่มีคำน้อยกว่า SAVE_EVERY_N ไม่เคย trigger autosave เลย
    processed_since_save = 0

    try:
        for level, words_list in data.items():
            if not isinstance(words_list, list):
                continue

            print(f"\n--- Processing CEFR Level: {level} ---")
            for i, item in enumerate(words_list):
                word = item.get('w')
                pos = item.get('pos')
                m_en = item.get('m_en')
                m_th = item.get('m_th')

                # 🌟 ถ้ามีป้าย is_fixed แปลว่าทำเสร็จแล้ว ให้ข้ามไปเลย
                if item.get('is_fixed') == True:
                    continue

                timestamp = time.strftime('%H:%M:%S')
                print(f"[{timestamp}] [{i+1}/{len(words_list)}] Fixing: '{word}' ... ", end="", flush=True)

                start_time = time.time()
                fixed_data = get_fixed_data(word, pos, m_en)
                elapsed = time.time() - start_time

                if fixed_data:
                    item['m_en'] = fixed_data.get('m_en', m_en)
                    item['m_th'] = fixed_data.get('m_th', m_th)
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
