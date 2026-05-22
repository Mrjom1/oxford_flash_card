// ดึง version / cache names จาก config.js จุดเดียว
importScripts('./config.js');
// ตอนนี้ APP_VERSION, APP_CACHE, STROKE_CACHE, STROKE_LIMIT พร้อมใช้แล้ว

const PRECACHE_ASSETS = [
    './index.html',
    './manifest.json',
    './info.json',
    './config.js'   // precache config ด้วยเสมอ
];

// ── Install: cache app shell ──────────────────────────────────────────────────
self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(APP_CACHE).then(cache => cache.addAll(PRECACHE_ASSETS))
    );
    self.skipWaiting();
});

// ── Activate: ทุบ cache เวอร์ชันเก่าทิ้ง ─────────────────────────────────────
self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys
                    .filter(k => k !== APP_CACHE && k !== STROKE_CACHE)
                    .map(k => caches.delete(k))
            )
        )
    );
    self.clients.claim();
});

// ── Fetch: Runtime caching แบบแยก strategy ───────────────────────────────────
self.addEventListener('fetch', e => {
    const url = e.request.url;

    // Stroke character data → cache แยก + FIFO cap
    if (url.includes('hanzi-writer-data')) {
        e.respondWith(handleStrokeCache(e.request));
        return;
    }

    // ทุกอย่างอื่น → cache-first, network fallback
    e.respondWith(
        caches.match(e.request).then(cached => {
            if (cached) return cached;

            return fetch(e.request).then(res => {
                const shouldCache =
                    url.includes('words_') ||                    // vocab JSON ทุกภาษา
                    url.includes('hanzi-writer.min.js');         // Hanzi Writer library

                if (shouldCache) {
                    caches.open(APP_CACHE)
                        .then(c => c.put(e.request, res.clone()));
                }
                return res;
            }).catch(() => new Response('', {
                status: 404,
                statusText: 'Offline and asset not cached'
            }));
        })
    );
});

// ── handleStrokeCache: FIFO เพื่อไม่ให้ cache บวม ────────────────────────────
async function handleStrokeCache(request) {
    const cache = await caches.open(STROKE_CACHE);
    const cached = await cache.match(request);
    if (cached) return cached;  // hit → คืนทันที

    try {
        const response = await fetch(request);
        if (!response.ok) return response;

        const keys = await cache.keys();
        if (keys.length >= STROKE_LIMIT) {
            await cache.delete(keys[0]); // ลบรายการเก่าสุด (FIFO)
        }

        await cache.put(request, response.clone());
        return response;
    } catch {
        return new Response('', { status: 404, statusText: 'Offline' });
    }
}