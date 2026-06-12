<div align="center">

# 🌐 VocabEcosystem PWA

**International Polyglot Vocabulary Edition**

[![Version](https://img.shields.io/badge/version-v3.54-38BDF8?style=flat-square)](https://github.com/)
[![License](https://img.shields.io/badge/license-MIT-34D399?style=flat-square)](LICENSE)
[![PWA](https://img.shields.io/badge/PWA-ready-818CF8?style=flat-square)](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
[![Client-Only](https://img.shields.io/badge/backend-none-FBBF24?style=flat-square)](#)

ระบบท่องจำคำศัพท์ 3 ภาษา · ทำงาน offline · ติดตั้งเป็นแอปได้

[🚀 Demo](#deploy) · [📖 คู่มือใช้งาน](#-คู่มือใช้งาน) · [📂 สเปกไฟล์ข้อมูล](#-สเปกไฟล์คำศัพท์) · [📝 Changelog](#-changelog)

</div>

---

## 💡 Concept

VocabEcosystem เป็น **Progressive Web App แบบ Client-Driven 100%** — ไม่มี backend ไม่มี server ไม่ต้อง login ข้อมูลทั้งหมดอยู่บนเครื่องของผู้ใช้

ออกแบบมาเพื่อให้ท่องศัพท์ 3 ภาษาในแอปเดียว พร้อมสถิติและความก้าวหน้าแยกอิสระต่อภาษา รองรับทั้ง Desktop และ Mobile ทำงาน offline ได้ผ่าน Service Worker

```
ภาษาอังกฤษ (CEFR A1–C2)  ·  ภาษาจีน (HSK 3.0 HSK1–7)  ·  ภาษาญี่ปุ่น (JLPT N5–N1)
```

---

## ✨ Features

| Feature | รายละเอียด |
|---|---|
| 🌐 **Multi-Language** | อังกฤษ CEFR / จีน HSK 3.0 / ญี่ปุ่น JLPT — สถิติแยกอิสระต่อภาษา |
| 🃏 **Smart Flashcards** | บัตรคำพร้อมคำอ่านเฉพาะภาษา (Phonetics / Pinyin / Kana) แอนิเมชัน 3D flip |
| 🎙️ **AI Voice Evaluator** | ฝึกออกเสียง ตรวจคะแนน Real-time ด้วยอัลกอริทึม Edit Distance |
| 🧠 **Spaced Repetition (SRS)** | คัดคำที่ลืมบ่อยขึ้นมาทบทวนซ้ำอัตโนมัติ |
| ⚡ **Speed Challenge** | โหมดแข่งเวลา 60 วินาที — บันทึก high score ต่อภาษา |
| 🎬 **Anime Voice Search** | เปิดไมค์แกะเสียงอนิเมะ → เดาคำศัพท์ที่ตรง (maxAlternatives = 5) |
| 🔍 **Thai-to-Target Search** | ค้นคำศัพท์ย้อนกลับจากภาษาไทย รองรับพิมพ์และพูด |
| ✍️ **Stroke Order** | ดูลำดับเส้นพู่กัน (จีน + Kanji) สลับดูหลายตัวอักษร + โหมดวาดตาม / วาดเอง |
| 🔔 **Smart Reminders** | แจ้งเตือนส่วนบุคคล สูงสุด 4 ช่วงเวลา |
| 📦 **PWA + Offline** | ติดตั้งเป็นแอปได้ ทำงาน offline ผ่าน Service Worker |

---

## 🚀 คู่มือใช้งาน

### 1. เริ่มใช้งาน

เปิดเว็บผ่าน Browser ได้เลย ไม่ต้องติดตั้ง — หรือกด **"ติดตั้งเป็นแอป"** บน Android/iOS เพื่อใช้งาน offline

```bash
# สำหรับ dev ทดสอบ local
npx serve .
# หรือ
python3 -m http.server 8080
```

> ⚠️ ต้องเปิดผ่าน **HTTPS** เท่านั้น (Speech API + Service Worker ต้องการ secure context)

### 2. เลือกภาษาและระดับ

ไปที่ **⚙️ ตั้งค่า → เลือกสลับภาษาเรียน** จากนั้นเลือก Level ที่ bar ด้านบน (A1–C2 / HSK1–7 / N5–N1)

### 3. ท่องคำศัพท์ด้วย Flashcard

- **แตะการ์ด** → พลิกดูความหมาย
- กด **🔊 ฟัง** เพื่อฟังสำเนียง · กด **🎤 พูดเพื่อตรวจ** เพื่อฝึกออกเสียง
- ประเมินตัวเองด้วย 😓 ยาก / 🙂 พอได้ / ⭐ จำได้ — ระบบ SRS จะปรับลำดับให้อัตโนมัติ

### 4. โหมดแกะเสียงอนิเมะ 🎬

1. เปลี่ยนภาษาให้ตรงกับอนิเมะที่ดู (จีน / ญี่ปุ่น)
2. กดแท็บ **แกะเสียง/ค้นหา** → **แกะเสียงอนิเมะ**
3. จ่อไมค์ใกล้ลำโพง — แอปจะแสดงคำศัพท์ที่เสียงตรงกัน 5 อันดับ
4. แตะผลลัพธ์เพื่อ warp ไปที่การ์ดคำนั้นทันที

### 5. Stroke Order ✍️

เปิดการ์ดคำศัพท์ภาษาจีน / Kanji ญี่ปุ่น → กดปุ่ม **✍️** ที่หน้าการ์ด  
เลือก **วาดตาม** (มี guide) หรือ **วาดเอง** (ไม่มี guide) — สลับตัวอักษรด้วยปุ่ม ◀ ▶

---

## 📂 โครงสร้างไฟล์

```
VocabEcosystem/
├── config.js          ← ✏️ Single Source of Truth (version / cache names)
├── index.html         ← Main PWA shell + ทุก logic
├── sw.js              ← Service Worker
├── manifest.json      ← PWA manifest
├── info.json          ← App metadata (subtitle, features, donate)
├── icon-192.png       ← App icon (any)
├── icon-512.png       ← App icon (any)
├── icon-maskable-*.png← App icon (maskable, Android adaptive)
├── apple-touch-icon.png ← iOS home screen icon
├── words_en.json      ← คลังศัพท์ Oxford CEFR (A1–C2)     ← ต้องมี
├── words_zh.json      ← คลังศัพท์ HSK 3.0 (HSK1–HSK7)    ← ต้องมี
└── words_jp.json      ← คลังศัพท์ JLPT (N5–N1)           ← ต้องมี
```

---

## 📋 สเปกไฟล์คำศัพท์

### `words_en.json` — อังกฤษ CEFR

```json
{
  "A1": [
    {
      "w":    "apple",
      "ph":   "/ˈæp.əl/",
      "pos":  "noun",
      "m_th": "แอปเปิล",
      "m_en": "a round fruit with red or green skin",
      "ex":   ["I eat an apple every day.", "The apple is red."]
    }
  ]
}
```

| Field | ชนิด | คำอธิบาย |
|---|---|---|
| `w` | string | คำศัพท์ |
| `ph` | string | สัทอักษร IPA |
| `pos` | string | ประเภทคำ (noun / verb / adj …) |
| `m_th` | string | ความหมายภาษาไทย |
| `m_en` | string | ความหมายภาษาอังกฤษ |
| `ex` | string[] | ประโยคตัวอย่าง (1–2 ประโยค) |

### `words_zh.json` — จีน HSK 3.0

```json
{
  "HSK1": [
    {
      "w":           "你好",
      "pinyin":      "nǐ hǎo",
      "traditional": "你好",
      "pos":         "phrase",
      "m_th":        "สวัสดี",
      "m_en":        "Hello",
      "classifiers": [],
      "ex":          ["你好！", "你好，老师。"]
    }
  ]
}
```

เพิ่มจาก EN: `pinyin`, `traditional`, `classifiers[]`

### `words_jp.json` — ญี่ปุ่น JLPT

```json
{
  "N5": [
    {
      "w":    "食べる",
      "kana": "たべる",
      "pos":  "verb",
      "m_th": "กิน",
      "m_en": "to eat",
      "ex":   ["ご飯を食べる。", "毎日食べます。"]
    }
  ]
}
```

เพิ่มจาก EN: `kana` (คำอ่านฮิรางานะ)

---

## 🔢 Version Management

แก้เวอร์ชันที่ **`config.js` เพียงที่เดียว** — SW และ index.html รับค่าพร้อมกัน

```js
// config.js
var APP_VERSION  = 'v3.54';
var APP_CACHE    = 'oxford-vocab-' + APP_VERSION;
var STROKE_CACHE = 'oxford-stroke-v1';
var STROKE_LIMIT = 500;
```

---

## 🗄️ Cache Strategy

| Cache | ชื่อ | ขนาด | Strategy |
|---|---|---|---|
| App Shell + Vocab | `oxford-vocab-vX.XX` | ไม่จำกัด | Cache-First |
| Stroke Order | `oxford-stroke-v1` | สูงสุด 500 entries | FIFO Cap |

---

## 🌐 Browser Support

| Browser | Flashcard | Voice | Stroke | PWA Install |
|---|:---:|:---:|:---:|:---:|
| Chrome Android | ✅ | ✅ | ✅ | ✅ |
| Safari iOS 16+ | ✅ | ✅ | ✅ | ✅ |
| Chrome Desktop | ✅ | ✅ | ✅ | ✅ |
| Samsung Internet | ✅ | ✅ | ✅ | ✅ |
| Firefox | ✅ | ⚠️ | ✅ | ❌ |

---

## 🚀 Deploy

Static files ล้วน — ไม่ต้องการ backend

| Platform | วิธี |
|---|---|
| **Netlify** | Drag & drop folder หรือเชื่อม Git |
| **GitHub Pages** | Push ขึ้น repo → เปิด Pages |
| **Vercel** | `vercel --prod` หรือ import Git |

---

## 📝 Changelog

### v3.54 — Mobile Reliability Fixes
- 🔔 **Fix: Notification ไม่ขึ้นบน Android (Samsung ฯลฯ)** — เปลี่ยนจาก `new Notification()` (Android throw TypeError) ไปใช้ `registration.showNotification()` ผ่าน Service Worker + เพิ่ม `notificationclick` handler ใน sw.js
- 🔔 **Fix: timer แจ้งเตือนหายหลังปิดแอป** — เรียก `scheduleNotif()` ตอน boot และ re-schedule เมื่อกลับมา foreground (`visibilitychange`)
- 🔔 **UI แจ้งข้อจำกัด PWA** — บอก user ตรง ๆ ว่าแจ้งเตือนทำงานเฉพาะตอนแอปเปิดอยู่ (ข้อจำกัดของเว็บ client-only ไม่มี push server)
- 🔇 **Fix: ไม่มีเสียง TTS บนบางเครื่อง (Vivo / ROM จีน)** — เดิม fail เงียบ ตอนนี้ตรวจ `getVoices()` ว่าง + `utterance.onerror` แล้วแสดง toast แนะนำติดตั้ง Google Speech Services + normalize lang code `zh_CN` → `zh-CN`
- 🛡️ **sw.js: เช็ค `res.ok` ก่อน cache** — กัน cache error response (404/500) ค้างถาวรใน cache-first
- 🌐 **sw.js: Offline navigation fallback** — navigation request คืน `index.html` จาก cache (App Shell) แก้หน้าขาวตอน offline
- 🖼️ **PNG icons จริง** — แทน SVG data URI (Samsung Internet/launcher บางตัวไม่รองรับ) + แยก `purpose: any / maskable` + เพิ่ม `apple-touch-icon` สำหรับ iOS
- 🎨 ปรับ `background_color` / `theme_color` ใน manifest ให้ตรงกับ `theme-color` ใน index.html (`#0F172A`)

### v3.53 — UX Polish + Stroke Order Enhanced
- ✅ **iOS Safari banner** — แสดงคำแนะนำ "Share → Add to Home Screen" แทน (beforeinstallprompt ไม่ทำงานบน iOS)
- 🔢 **Level sorting** — `LEVEL_ORDER` ใน config.js กำหนดลำดับ A1→C2, HSK1→7, N5→N1 ทุกภาษา
- ✍️ **Stroke Order multi-char** — คำหลายตัวอักษร (เช่น 学習) มีปุ่ม ◀ ▶ + indicator "1/2"
- 🎮 **Stroke Quiz Mode** — วาดตาม (มี guide) / วาดเอง (ไม่มี guide) พร้อม feedback และนับ mistake
- 🐛 **Bug fix: Card flip** — แก้การ์ดแสดงคำแปลคำถัดไปแว่บหนึ่งก่อนหมุน
- 🏗️ **READING_FIELD + STROKE_LANGS** — เตรียมรองรับภาษาใหม่ในอนาคต (เกาหลี ฯลฯ)

### v3.52 — Stroke Order + Version Management
- ✨ เพิ่มฟีเจอร์ Stroke Order สำหรับจีนและ Kanji ญี่ปุ่น
- 🏗️ ย้าย version management ไปยัง `config.js`
- 🗄️ Stroke Cache แยกต่างหาก พร้อม FIFO cap (500 entries)
- 🖥️ แก้ Flag Emoji บน Windows Desktop
- 🔧 Cache Management UI ใน Settings

### v3.51 — Warm Pastel + Language Sandbox
- ย้าย Language Selector และ Theme Switcher ไปแท็บ Settings
- Language Prefixing — สถิติแยกอิสระต่อภาษา (`en_` / `zh_` / `jp_`)
- Light Mode โทนชานมพาสเทล มินิมอลสไตล์ญี่ปุ่น

---

## ☕ Support this project

If VocabEcosystem helped you learn, consider buying me a coffee in person ☕  
or sending a small crypto donation from anywhere in the world — any amount is appreciated 🙏

<table>
  <thead>
    <tr>
      <th align="center">Coin</th>
      <th align="left">Network</th>
      <th align="left">Address</th>
      <th align="center">QR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/32/color/usdt.png" width="22"/><br/><b>USDT</b></td>
      <td><code>BEP-20 (BSC)</code></td>
      <td><code>0x74AD7331CB8dA891406E0290BB90D51E2202d155</code></td>
      <td align="center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=0x74AD7331CB8dA891406E0290BB90D51E2202d155" width="75"/></td>
    </tr>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/32/color/eth.png" width="22"/><br/><b>ETH</b></td>
      <td><code>ERC-20</code></td>
      <td><code>0x74AD7331CB8dA891406E0290BB90D51E2202d155</code></td>
      <td align="center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=0x74AD7331CB8dA891406E0290BB90D51E2202d155" width="75"/></td>
    </tr>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/32/color/sol.png" width="22"/><br/><b>SOL</b></td>
      <td><code>Solana</code></td>
      <td><code>6o3odrTthz1PZSnXBMFPFuxvPRFDmiv3u5McLJ1ucAdR</code></td>
      <td align="center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=6o3odrTthz1PZSnXBMFPFuxvPRFDmiv3u5McLJ1ucAdR" width="75"/></td>
    </tr>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/32/color/doge.png" width="22"/><br/><b>DOGE</b></td>
      <td><code>Dogecoin</code></td>
      <td><code>DEz1yFkKRBpe8mYksEN59VVDJyJizwRcmT</code></td>
      <td align="center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=DEz1yFkKRBpe8mYksEN59VVDJyJizwRcmT" width="75"/></td>
    </tr>
  </tbody>
</table>

> ⭐ ไม่สะดวกโอน? การกด **Star** ให้โปรเจกต์ก็ช่วยได้มากเช่นกัน — ขอบคุณครับ!

---

## 📄 License

MIT © Shin@m0n Jom
