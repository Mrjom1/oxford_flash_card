# 🌐 Multi-Language VocabEcosystem PWA — v3.51 "The Refined Polyglot"

ระบบนิเวศน์ดิจิทัลแบบ Client-Driven 100% สำหรับท่องจำและทดสอบคำศัพท์สากล 3 ภาษาหลัก (อังกฤษ CEFR / จีน HSK 3.0 / ญี่ปุ่น JLPT) มาพร้อมระบบแยกโปรไฟล์สถิติอัจฉริยะ, ดีไซน์ Warm Pastel สบายสายตา และโหมดแกะรอยเสียงอนิเมะจากฮาร์ดแวร์ไมโครโฟนโดยตรง

---

## 🚀 สรุปรายการอัปเดตและแก้ไขในเวอร์ชัน v3.51

### 1. ย้ายตำแหน่ง Node ควบคุมสภาพแวดล้อม (Layout Clean-up)
* **ปัญหาเดิม:** ปุ่มเลือกภาษาและสวิตช์ธีมตรง Header ด้านบนเบียดบังกันและทับซ้อนเมื่อเปิดใช้งานบนหน้าจอสมาร์ตโฟนที่มีขนาดความกว้างจำกัด (เช่น Samsung Series)
* **การแก้ไข:** ย้าย `Language Dropdown` และ `Theme Switcher` ไปพำนักไว้ในแท็บ **⚙️ ตั้งค่า (Settings)** ภายใต้กรอบหัวข้อใหม่ *"🌐 สภาพแวดล้อมภาษา & ธีมแอป"* ทำให้ Header ด้านบนเหลือพื้นที่โปร่งโล่ง แสดงผลได้สะอาดตาทั้งใน Desktop และ Mobile 100%

### 2. ระบบคลังข้อมูลและสถิติแยกอิสระ (Isolated Language Sandbox)
* **ปัญหาเดิม:** สถิติจำศัพท์ได้/คำยาก, กราฟ 7 วัน, และข้อมูลระบบ SRS ถูกมัดรวมไว้ที่ LocalStorage คีย์เดียวกัน ส่งผลให้เมื่อผู้ใช้เปลี่ยนภาษา ข้อมูลความก้าวหน้าจะเกิดการทับซ้อนและตีกันมั่ว
* **การแก้ไข:** ใช้โครงสร้างสถาปัตยกรรม **Language Prefixing** (`en_` / `zh_` / `jp_`) ผูกติดกับฟังก์ชัน `reloadLanguageState()` ทุกครั้งที่มีการสลับภาษา แอปจะสลับโปรไฟล์ความจำชั่วคราว ดึงสถิติตลอดจนคำศัพท์ที่ผู้ใช้บันทึกเพิ่มแยกตามรายภาษาอย่างเด็ดขาด ส่งผลให้สามารถเรียนควบคู่ 2-3 ภาษาได้โดยที่สถิติไม่พัง

### 3. ชุบชีวิต Light Mode สไตล์ชานมพาสเทล (Cozy Pastel Palette)
* **ปัญหาเดิม:** โหมดสว่างในรุ่นทดลองมีความสว่างจ้าเกินไป และเกิดบั๊กสีพื้นหลังการ์ดไม่ยอมเปลี่ยนตามธีม ส่งผลให้ฟอนต์สีดำกลืนหายไปกับพื้นการ์ดมืด
* **การแก้ไข:** เปลี่ยนโทนสี Light Mode ใหม่ทั้งหมดให้เป็นสีชานมอุ่นพาสเทล มินิมอลสไตล์ญี่ปุ่น (`#F5F2EB`) เปลี่ยนการควบคุมพื้นหลังการ์ดจาก Hardcoded CSS ไปผูกติดกับตัวแปร CSS Variables (`--card-front-grad`) ทำให้การ์ดเปลี่ยนเป็นสีครีมนวลทันทีเมื่อสลับธีม พร้อมขลิบเส้นขอบปุ่มและชิปเลเวล (`--btn-border`) ให้เด่นชัดเห็นขอบเขตชัดเจนในที่สว่าง

---

## 📂 รายละเอียดสเปกไฟล์ฐานข้อมูลคำศัพท์ (Data Asset Requirements)

แอปพลิเคชันเวอร์ชัน v3.51 ขับเคลื่อนด้วยโครงสร้างไฟล์ JSON 3 ตัวหลักที่บันทึกคำแปลภาษาไทยเสร็จสิ้นจากระบบ Node.js:
1. `words_en.json` : คลังศัพท์ Oxford พากย์อังกฤษสากล แบ่งกล่อง `A1` ถึง `C2` (ระบบตั้งค่าให้โหลดไฟล์นี้เป็น Default แรกสุดเมื่อติดตั้งแอปครั้งแรก)
2. `words_zh.json` : คลังศัพท์จีนระบบใหม่ HSK 3.0 แบ่งกล่อง `HSK1` ถึง `HSK7` พร้อมฟิลด์ `pinyin`, `traditional`, และ `classifiers`
3. `words_jp.json` : คลังศัพท์ญี่ปุ่นสอบวัดระดับ แบ่งกล่อง `N5` ถึง `N1` พร้อมฟิลด์คำอ่านฮิรางานะล้วน `kana`

---

## 🎙️🎬 วิธีการใช้งานฟีเจอร์ "โหมดแกะเสียงอนิเมะ"
1. เข้าไปที่แท็บที่ 3 ด้านล่างสุด **"🎬 แกะเสียง/ค้นหา"**
2. เลือกเปลี่ยนสภาพแวดล้อมภาษาในหน้าตั้งค่าให้ตรงกับอนิเมะที่กำลังรับชม (เช่น สลับเป็นภาษาจีน ZH หรือ ญี่ปุ่น JP)
3. กดปุ่ม **"แกะเสียงอนิเมะ"** บนหน้าจอ ตัวแอปจะเปิดไมโครโฟนรับเสียง พร้อมสั่งการกลไกเดาคำพ้องเสียงล่วงหน้าถึง 5 อันดับ (`maxAlternatives = 5`)
4. เมื่อได้ผลลัพธ์คำศัพท์ที่เสียงตรงกัน ระบบจะสแกนคลัง JSON และดึงรายชื่อคำศัพท์พร้อมความหมายไทยขึ้นมาแสดงเป็น Candidate Card ทันที โดยผู้ใช้สามารถจิ้มที่การ์ดผลลัพธ์เพื่อ "วาร์ป" กลับไปท่องจำในหน้าต่างหลักได้ทันที

---

## ☕ Support this project

If VocabEcosystem helped you learn, consider buying me a coffee — or sending a small crypto donation from anywhere in the world. Any amount is appreciated. 🙏

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
      <td align="center"><img src="https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/32/color/usdt.png" width="22" alt="USDT"/><br/><b>USDT</b></td>
      <td><code>BEP-20 (BSC)</code></td>
      <td><code>0x74AD7331CB8dA891406E0290BB90D51E2202d155</code></td>
      <td align="center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=0x74AD7331CB8dA891406E0290BB90D51E2202d155" width="75" alt="QR"/></td>
    </tr>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/32/color/eth.png" width="22" alt="ETH"/><br/><b>ETH</b></td>
      <td><code>ERC-20 (Ethereum)</code></td>
      <td><code>0x74AD7331CB8dA891406E0290BB90D51E2202d155</code></td>
      <td align="center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=0x74AD7331CB8dA891406E0290BB90D51E2202d155" width="75" alt="QR"/></td>
    </tr>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/32/color/sol.png" width="22" alt="SOL"/><br/><b>SOL</b></td>
      <td><code>Solana</code></td>
      <td><code>6o3odrTthz1PZSnXBMFPFuxvPRFDmiv3u5McLJ1ucAdR</code></td>
      <td align="center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=6o3odrTthz1PZSnXBMFPFuxvPRFDmiv3u5McLJ1ucAdR" width="75" alt="QR"/></td>
    </tr>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/32/color/doge.png" width="22" alt="DOGE"/><br/><b>DOGE</b></td>
      <td><code>Dogecoin</code></td>
      <td><code>DEz1yFkKRBpe8mYksEN59VVDJyJizwRcmT</code></td>
      <td align="center"><img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=DEz1yFkKRBpe8mYksEN59VVDJyJizwRcmT" width="75" alt="QR"/></td>
    </tr>
  </tbody>
</table>

> ⭐ ไม่สะดวกโอน? การกด **Star** ให้โปรเจกต์ก็ช่วยได้มากเช่นกัน — ขอบคุณครับ!