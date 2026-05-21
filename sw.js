const CACHE_NAME = 'oxford-vocab-v3.5.1'; // 🔥 ปรับเป็น version.js เพื่อทุบแคชเก่า และบังคับอัปเดตหน้าจอชานมพาสเทลทันที

// 1. เก็บเฉพาะ "App Shell" หรือโครงสร้างหลักของแอปไว้ล่วงหน้า
const PRECACHE_ASSETS = [
    './index.html',
    './manifest.json',
    './info.json'
];

// ขั้นตอน Install: โหลดเฉพาะไฟล์โครงสร้างหลัก
self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_ASSETS))
    );
    self.skipWaiting();
});

// ขั้นตอน Activate: ล้าง Cache เวอร์ชันเก่าๆ (v3.5 / v3.50) ทิ้งทั้งหมดทันที
self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

// ขั้นตอน Fetch: ตรวจจับการดึงข้อมูล และทำระบบ Runtime Caching แยกไฟล์คำศัพท์ 3 ภาษา
self.addEventListener('fetch', e => {
    e.respondWith(
        caches.match(e.request).then(cachedResponse => {
            // 1. ถ้ามีใน Cache แล้ว ให้ดึงมาแสดงผลทันที (ทำงานออฟไลน์ได้)
            if (cachedResponse) {
                return cachedResponse;
            }

            // 2. ถ้ายังไม่มีใน Cache ให้ไปดึงจากเน็ตมาแสดง
            return fetch(e.request).then(networkResponse => {
                // เช็กว่าเป็นไฟล์คำศัพท์ที่มี Prefix ขึ้นต้นด้วย words_ หรือไม่
                if (e.request.url.includes('words_')) {
                    // แอบบันทึกไฟล์คำศัพท์ภาษานั้นๆ ลงคลังแคชของผู้ใช้แบบ On-Demand
                    return caches.open(CACHE_NAME).then(cache => {
                        cache.put(e.request, networkResponse.clone());
                        return networkResponse;
                    });
                }
                return networkResponse;
            }).catch(() => {
                return new Response('', { status: 404, statusText: 'Offline and asset not cached' });
            });
        })
    );
});