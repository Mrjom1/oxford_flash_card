/**
 * config.js — Single Source of Truth
 * VocabEcosystem PWA
 *
 * ✏️  แก้ที่นี่ที่เดียว — SW, index.html รับค่าพร้อมกันอัตโนมัติ
 *     ใช้ var (ไม่ใช่ const/let) เพื่อให้ sw.js โหลดผ่าน importScripts() ได้
 */

var APP_VERSION  = 'v3.53';
var APP_CACHE    = 'oxford-vocab-' + APP_VERSION;
var STROKE_CACHE = 'oxford-stroke-v1';
var STROKE_LIMIT = 500;

// ลำดับ Level ง่าย → ยาก แต่ละภาษา
var LEVEL_ORDER = {
    en: ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'],
    zh: ['HSK1', 'HSK2', 'HSK3', 'HSK4', 'HSK5', 'HSK6', 'HSK7'],
    jp: ['N5', 'N4', 'N3', 'N2', 'N1'],
    ko: ['TOPIK1', 'TOPIK2', 'TOPIK3', 'TOPIK4', 'TOPIK5', 'TOPIK6']
};

// ภาษาที่รองรับ Stroke Order
var STROKE_LANGS = ['zh', 'jp'];

// field คำอ่านของแต่ละภาษา
var READING_FIELD = {
    en: 'ph',
    zh: 'pinyin',
    jp: 'kana',
    ko: 'romanization'
};
