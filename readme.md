# 🌐 VocabEcosystem PWA

> **International Polyglot Vocabulary Edition** — v3.52  
> by Shin@m0n Jom

ระบบนิเวศน์ดิจิทัลแบบ **Client-Driven 100%** สำหรับท่องจำและทดสอบคำศัพท์สากล 3 ภาษาหลัก  
อังกฤษ (CEFR) · จีน (HSK 3.0) · ญี่ปุ่น (JLPT) — ทำงานเป็น PWA ได้ทั้งบน Desktop และ Mobile

---

## ✨ Features

| Feature | รายละเอียด |
|---|---|
| 🌐 Multi-Language | อังกฤษ CEFR / จีน HSK 3.0 / ญี่ปุ่น JLPT พร้อมสถิติแยกอิสระต่อภาษา |
| 🃏 Smart Flashcards | บัตรคำพร้อมคำอ่านเฉพาะภาษา (Phonetics / Pinyin / Kana) |
| 🎙️ AI Voice Evaluator | ตรวจคะแนนออกเสียงแบบ Real-time ด้วยอัลกอริทึม Edit Distance |
| 🧠 Spaced Repetition | SRS อัจฉริยะ คัดคำที่ลืมบ่อยขึ้นมาทบทวนซ้ำ |
| ⚡ Speed Challenge | ตอบคำถามแข่งเวลา 60 วินาที |
| 🎬 Anime Voice Search | แกะเสียงอนิเมะ เปิดไมค์แล้วเดาคำศัพท์ (maxAlternatives = 5) |
| 🔍 Thai-to-Target Search | ค้นคำศัพท์ย้อนกลับจากภาษาไทย รองรับพิมพ์และพูด |
| ✍️ Stroke Order | ดูลำดับการลากเส้นพู่กัน (จีน + Kanji ญี่ปุ่น) ผ่าน Hanzi Writer |
| 🔔 Smart Reminders | แจ้งเตือนส่วนบุคคล สูงสุด 4 ช่วงเวลา |
| 📦 PWA + Offline | ติดตั้งเป็นแอปได้ ทำงาน offline ผ่าน Service Worker |

---

## 📂 โครงสร้างไฟล์

```
VocabEcosystem/
├── config.js          ← ✏️ Single Source of Truth (version / cache names)
├── index.html         ← Main PWA shell + ทุก logic
├── sw.js              ← Service Worker (importScripts config.js)
├── manifest.json      ← PWA manifest
├── info.json          ← App metadata (subtitle, features)
├── words_en.json      ← คลังศัพท์ Oxford CEFR (A1–C2)       ← ต้องมี
├── words_zh.json      ← คลังศัพท์ HSK 3.0 (HSK1–HSK7)       ← ต้องมี
└── words_jp.json      ← คลังศัพท์ JLPT (N5–N1)              ← ต้องมี
```

---

## 📋 สเปกไฟล์คำศัพท์ (Data Format)

### `words_en.json`
```json
{
  "A1": [
    {
      "w": "apple",
      "ph": "/ˈæp.əl/",
      "pos": "noun",
      "m_th": "แอปเปิล",
      "m_en": "a round fruit",
      "ex": ["I eat an apple every day.", "The apple is red."]
    }
  ],
  "A2": [ ... ],
  "B1": [ ... ]
}
```

### `words_zh.json`
```json
{
  "HSK1": [
    {
      "w": "你好",
      "pinyin": "nǐ hǎo",
      "traditional": "你好",
      "pos": "phrase",
      "m_th": "สวัสดี",
      "m_en": "Hello",
      "classifiers": [],
      "ex": ["你好！", "你好，老师。"]
    }
  ]
}
```

### `words_jp.json`
```json
{
  "N5": [
    {
      "w": "食べる",
      "kana": "たべる",
      "pos": "verb",
      "m_th": "กิน",
      "m_en": "to eat",
      "ex": ["ご飯を食べる。", "毎日食べます。"]
    }
  ]
}
```

---

## 🔢 Version Management

แก้เวอร์ชันที่ **`config.js` เพียงไฟล์เดียว** — SW และ index.html จะรับค่าพร้อมกัน

```js
// config.js
var APP_VERSION  = 'v3.52';   // ← แก้ตรงนี้
var APP_CACHE    = 'oxford-vocab-' + APP_VERSION;
var STROKE_CACHE = 'oxford-stroke-v1';
var STROKE_LIMIT = 800;
```

> **หมายเหตุ:** ทุกครั้งที่เปลี่ยน `APP_VERSION`, SW จะ activate ทันทีและล้าง cache เวอร์ชันเก่าโดยอัตโนมัติ

---

## 🗄️ Cache Strategy

| Cache | ชื่อ | ขนาดสูงสุด | Strategy |
|---|---|---|---|
| App Shell + Vocab | `oxford-vocab-vX.XX` | ไม่จำกัด (vocab JSON ≈ 1–2 MB) | Cache-First |
| Stroke Order Data | `oxford-stroke-v1` | 800 entries ≈ 2.4 MB | FIFO Cap |

ผู้ใช้สามารถดูและล้าง Stroke Cache ได้จาก **⚙️ ตั้งค่า → จัดการพื้นที่ Cache**

---

## ✍️ Stroke Order (Hanzi Writer)

- Library: [Hanzi Writer](https://hanziwriter.org/) v3.5 · MIT License  
- รองรับ: จีน (CJK Unified) ทุกตัว · ญี่ปุ่น (Kanji) เท่านั้น  
- ไม่รองรับ: Hiragana / Katakana (ไม่มีใน database)  
- โหลด library แบบ lazy (เฉพาะตอนกดปุ่มครั้งแรก)  
- Prefetch stroke data อัตโนมัติเมื่อเปลี่ยน Level ขณะออนไลน์

---

## 🚀 Deploy

แอปนี้เป็น **static files ล้วน** ไม่ต้องการ backend

```bash
# Local dev
npx serve .
# หรือ
python3 -m http.server 8080
```

**Static Hosting ที่แนะนำ:**
- [GitHub Pages](https://pages.github.com/) — ฟรี, รองรับ HTTPS
- [Netlify](https://netlify.com/) — drag & drop deploy
- [Vercel](https://vercel.com/) — เชื่อมต่อ git โดยตรง

> ⚠️ ต้องเปิดผ่าน **HTTPS** เท่านั้น (Service Worker + Speech API ต้องการ secure context)

---

## 🌐 Browser Support

| Browser | Flashcard | Voice | Stroke Order | PWA Install |
|---|---|---|---|---|
| Chrome (Android) | ✅ | ✅ | ✅ | ✅ |
| Safari (iOS 16+) | ✅ | ✅ | ✅ | ✅ |
| Chrome (Desktop) | ✅ | ✅ | ✅ | ✅ |
| Firefox | ✅ | ⚠️ บางฟีเจอร์ | ✅ | ❌ |
| Samsung Internet | ✅ | ✅ | ✅ | ✅ |

---

## 📝 Changelog

### v3.52 — Stroke Order + Version Management
- ✨ เพิ่มฟีเจอร์ **Stroke Order** (ลำดับเส้น) สำหรับภาษาจีนและ Kanji ญี่ปุ่น  
- 🏗️ ย้าย version management ไปยัง `config.js` (Single Source of Truth)  
- 🗄️ เพิ่ม Stroke Cache แยกต่างหากพร้อม FIFO cap (500 entries ≈ 1.5 MB)  
- 🖥️ แก้ไข Flag Emoji ไม่แสดงบน Windows Desktop ใน dropdown  
- 🔧 เพิ่ม Cache Management UI ใน Settings

### v3.51 — Warm Pastel + Language Sandbox
- ย้าย Language Selector และ Theme Switcher ไปยังแท็บ Settings  
- Language Prefixing สำหรับสถิติแยกอิสระต่อภาษา (`en_` / `zh_` / `jp_`)  
- Light Mode โทนชานมพาสเทล มินิมอลสไตล์ญี่ปุ่น

---

## 📄 License

MIT © Shin@m0n Jom