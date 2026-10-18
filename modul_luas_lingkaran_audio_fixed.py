# -*- coding: utf-8 -*-
"""
MODUL INTERAKTIF LUAS LINGKARAN - KELAS VI SD/MI
Jalankan:  streamlit run app.py

Struktur file:
  1. KONFIGURASI GURU        -> identitas sekolah, KKM, tautan video, PIN guru
  2. BANK MATERI & TOPIK     -> langkah materi + rekomendasi adaptif
  3. BANK SOAL               -> 10 soal pilihan ganda + 5 soal esai (mudah diedit)
  4. FUNGSI PENILAIAN        -> logika murni (tanpa Streamlit)
  5. TAMPILAN (UI)           -> CSS pink-biru-kuning, latar, musik/suara, halaman-halaman, router

Data siswa hanya disimpan di st.session_state (sementara, selama sesi berjalan).
"""
import html
import base64
import json
import math
import re
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# 1. KONFIGURASI GURU  (EDIT BAGIAN INI)
# ============================================================
NAMA_SEKOLAH = ""
NAMA_GURU = "[ISI: Nama Guru]"                       # TODO GURU
KKM = 75                                             # TODO GURU: batas ketuntasan (0-100)
GURU_PIN = "guru123"                                 # TODO GURU: ganti PIN panel guru

# Tautan video. Kosongkan ("") jika belum ada; aplikasi akan menampilkan placeholder.
# Contoh format: "https://www.youtube.com/watch?v=XXXXXXXXXXX"
VIDEO_UTAMA = ""                                     # TODO GURU: video materi inti
VIDEO_PENCARIAN = "https://www.youtube.com/results?search_query=luas+lingkaran+kelas+6+SD"

# TODO GURU: ganti dengan rumusan CP/tujuan resmi dari LKPD / kurikulum sekolah.
CAPAIAN_PEMBELAJARAN = [
    "Mengenali jari-jari dan diameter lingkaran.",
    "Menjelaskan hubungan diameter dan jari-jari.",
    "Memilih nilai π yang sesuai untuk perhitungan.",
    "Menghitung luas lingkaran jika diketahui jari-jari atau diameter.",
    "Menyelesaikan masalah luas lingkaran dalam kehidupan sehari-hari.",
    "Menjelaskan langkah penyelesaian dengan bahasamu sendiri.",
]

LETTERS = "ABCD"

# ============================================================
# 2. BANK MATERI & TOPIK REKOMENDASI
# ============================================================
# Urutan langkah Materi Inti (indeks dipakai oleh tombol rekomendasi).
MATERI_STEPS = [
    ("⭕", "Mengenal lingkaran"),            # 0
    ("↔️", "Jari-jari dan diameter"),         # 1
    ("📐", "Rumus luas lingkaran"),          # 2
    ("🔢", "Nilai π (pi)"),                  # 3
    ("🧮", "Contoh soal dan penyelesaian"),  # 4
    ("🎛️", "Coba sendiri: alat hitung"),     # 5
    ("🎬", "Video pembelajaran"),            # 6
]

# Setiap topik terhubung ke satu langkah materi. Isi "video" dengan tautan jika ada.
TOPICS = {
    "unsur": {
        "label": "Titik pusat, jari-jari, dan diameter",
        "step": 0, "video": "",               # TODO GURU: tautan video topik ini
        "tip": "Ulangi bagian unsur-unsur lingkaran: titik pusat, jari-jari, dan diameter.",
    },
    "hubungan": {
        "label": "Hubungan jari-jari dan diameter",
        "step": 1, "video": "",               # TODO GURU
        "tip": "Ingat: d = 2 × r dan r = d ÷ 2. Cari jari-jari lebih dulu sebelum memakai rumus luas.",
    },
    "rumus": {
        "label": "Rumus luas lingkaran",
        "step": 2, "video": "",               # TODO GURU
        "tip": "Luas lingkaran: L = π × r × r. Jangan tertukar dengan rumus keliling (2 × π × r).",
    },
    "pi": {
        "label": "Memilih nilai π",
        "step": 3, "video": "",               # TODO GURU
        "tip": "Pakai π = 22/7 jika r atau d kelipatan 7; pakai π = 3,14 untuk ukuran lainnya.",
    },
    "hitung": {
        "label": "Contoh perhitungan luas lingkaran",
        "step": 4, "video": "",               # TODO GURU
        "tip": "Pelajari contoh penyelesaian langkah demi langkah, lalu perhatikan perkaliannya.",
    },
    "cerita": {
        "label": "Luas lingkaran dalam soal cerita",
