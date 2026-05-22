/**
 * config.js — Single Source of Truth
 * VocabEcosystem PWA
 *
 * ✏️  แก้ที่นี่ที่เดียว — SW, index.html จะรับค่าพร้อมกันอัตโนมัติ
 *     ใช้ var (ไม่ใช่ const/let) เพื่อให้ sw.js โหลดผ่าน importScripts() ได้
 */

var APP_VERSION = 'v3.52';                          // ← แก้ตรงนี้จุดเดียว
var APP_CACHE = 'oxford-vocab-' + APP_VERSION;    // cache หลัก (vocab + shell)
var STROKE_CACHE = 'oxford-stroke-v1';               // cache stroke data (แยกต่างหาก)
var STROKE_LIMIT = 800;                              // จำนวน entry สูงสุด ≈ 2.4 MB