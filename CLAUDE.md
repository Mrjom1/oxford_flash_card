# VocabEcosystem PWA — Project Instructions

## ภาพรวม
Progressive Web App ท่องคำศัพท์ 3 ภาษา (อังกฤษ CEFR / จีน HSK 3.0 / ญี่ปุ่น JLPT) แบบ client-only 100%
ไม่มี backend ไม่มี login ข้อมูลอยู่บนเครื่องผู้ใช้ทั้งหมด ทำงาน offline ผ่าน Service Worker ติดตั้งเป็นแอปได้

## สถาปัตยกรรม / ไฟล์หลัก
- `config.js` — Single Source of Truth (version, cache names, LEVEL_ORDER, READING_FIELD, STROKE_LANGS) ใช้ `var` เท่านั้น เพราะ sw.js โหลดผ่าน `importScripts()`
- `index.html` — PWA shell + logic ทั้งหมดอยู่ในไฟล์เดียว (~118KB)
- `sw.js` — Service Worker (cache strategy)
- `manifest.json` — PWA manifest
- `info.json` — metadata (subtitle, features, donate)
- `words_en/zh/jp.json` — คลังศัพท์ (ต้องมีครบทั้ง 3)

## Data schema
ทุกภาษา: `w, pos, m_th, m_en, ex[]`
- EN เพิ่ม `ph`
- ZH เพิ่ม `pinyin, traditional, classifiers[]`
- JP เพิ่ม `kana`

## Cache strategy
- App+Vocab = `oxford-vocab-vX.XX` (Cache-First, ไม่จำกัด)
- Stroke = `oxford-stroke-v1` (FIFO cap 500)

## กฎสำคัญ
- แก้เวอร์ชันที่ `config.js` **ที่เดียว** — SW และ index.html รับค่าพร้อมกัน ทุกครั้งที่ release ต้อง bump `APP_VERSION`
- ต้องรันผ่าน HTTPS (Speech API + SW ต้องการ secure context)
- โครงสร้างเตรียมรองรับภาษาที่ 4 (เกาหลี TOPIK) ไว้แล้วใน config
- อัปเดต Changelog ใน `readme.md` และ badge version ทุก release

## Working rules (ระหว่างทำงานกับผู้ใช้)
- แนะนำแนวทางและ **confirm ก่อนลง code ทุกครั้ง** ไม่แก้ไฟล์เองก่อนตกลง
- ตอบเป็นภาษาไทย, กระชับแต่ครบ, ถามทีละคำถาม
- หลังมีการ update ให้ **แจ้งคำสั่ง git ต่อท้าย** (add/commit/push) พร้อม commit message ที่แนะนำ
- เมื่อ **context ใกล้เต็ม แจ้งทันที** พร้อมสรุปประเด็นสำคัญไว้ต่อใน chat ใหม่
- ทำงานต่อเนื่องกับ git history เดิม (branch `main`, remote `origin`)
