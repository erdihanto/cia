import streamlit as st
import random
import time

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="ARCADE MATEMATIKA CYBER", page_icon="🎮", layout="centered")

# 2. Gaya Desain Custom CSS (Retro Arcade / Neon Cyberpunk)
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0e15;
        color: #00ff66;
        font-family: 'Courier New', Courier, monospace;
    }
    .judul-neon {
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
        color: #fff;
        text-shadow: 0 0 10px #ff0055, 0 0 20px #ff0055, 0 0 30px #ff0055;
        margin-bottom: 5px;
    }
    .sub-judul {
        text-align: center;
        color: #00ffff;
        font-size: 1.1rem;
        text-shadow: 0 0 5px #00ffff;
        margin-bottom: 30px;
    }
    .kotak-soal {
        background-color: #1a1c28;
        border: 3px solid #00ffff;
        box-shadow: 0 0 15px #00ffff;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #ffff00;
        text-shadow: 0 0 5px #ffff00;
        margin-bottom: 25px;
    }
    .papan-skor {
        background: linear-gradient(90deg, #ff0055, #00ffff);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: bold;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    div.stButton > button {
        background-color: #1a1c28 !important;
        color: #00ff66 !important;
        border: 2px solid #00ff66 !important;
        box-shadow: 0 0 8px #00ff66 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 12px 0px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #00ff66 !important;
        color: #000000 !important;
        box-shadow: 0 0 20px #00ff66 !important;
        transform: scale(1.02);
    }
    /* Tombol Mode & Keluar */
    .stButton button[key^="menu_"], .stButton button[key^="mode_"], .stButton button[key="btn_kembali"] {
        border: 2px solid #ff0055 !important;
        color: #ff0055 !important;
        box-shadow: 0 0 8px #ff0055 !important;
    }
    .stButton button[key^="menu_"]:hover, .stButton button[key^="mode_"]:hover, .stButton button[key="btn_kembali"]:hover {
        background-color: #ff0055 !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px #ff0055 !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="judul-neon">⚡ MULTIPLIER ARCADE ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-judul">> SYSTEM READY: HANCURKAN TANTANGAN MATEMATIKA!</div>', unsafe_allow_html=True)

# 3. Inisialisasi State / Data Game
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'mode' not in st.session_state:
    st.session_state.mode = None # 'perkalian' atau 'pertambahan'
if 'skor' not in st.session_state:
    st.session_state.skor = 0
if 'nyawa' not in st.session_state:
    st.session_state.nyawa = 3
if 'angka_tetap' not in st.session_state:
    st.session_state.angka_tetap = 1
if 'pengali' not in st.session_state:
    st.session_state.pengali = random.randint(1, 10)
if 'pilihan_jawaban' not in st.session_state:
    st.session_state.pilihan_jawaban = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'tipe_feedback' not in st.session_state:
    st.session_state.tipe_feedback = "info"

def buat_pilihan_ganda(kunci_jawaban):
    pilihan = {kunci_jawaban}
    while len(pilihan) < 4:
        salah = kunci_jawaban + random.randint(-4, 4)
        if salah >= 0 and salah != kunci_jawaban:
            pilihan.add(salah)
    list_pilihan = list(pilihan)
    random.shuffle(list_pilihan)
    return list_pilihan

# --- TAMPILAN 1: PILIH MODE UTAMA (PERKALIAN / PERTAMBAHAN) ---
if not st.session_state.game_started and st.session_state.mode is None:
    st.markdown("<h3 style='text-align:center; color:#fff;'>[ PILIH MODE OPERASI ]</h3>", unsafe_allow_html=True)
    st.write("")
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        if st.button("❌ MODE PERKALIAN", use_container_width=True, key="mode_kali"):
            st.session_state.mode = "perkalian"
            st.rerun()
    with col_mode2:
        if st.button("➕ MODE PERTAMBAHAN", use_container_width=True, key="mode_tambah"):
            st.session_state.mode = "pertambahan"
            st.rerun()

# --- TAMPILAN 2: PILIH ANGKA DASAR (1 - 10) ---
elif not st.session_state.game_started and st.session_state.mode is not None:
    st.markdown(f"<h3 style='text-align:center; color:#fff;'>[ PILIH ANGKA {st.session_state.mode.upper()} ]</h3>", unsafe_allow_html=True)
    st.write("")
    
    # Grid tombol angka 1 sampai 10
    simbol = "❌" if st.session_state.mode == "perkalian" else "➕"
    
    rows = [st.columns(5), st.columns(5)]
    for i in range(1, 11):
        row_idx = 0 if i <= 5 else 1
        col_idx = (i - 1) % 5
        with rows[row_idx][col_idx]:
            if st.button(f"{simbol} {i}", use_container_width=True, key=f"menu_{i}"):
                st.session_state.angka_tetap = i
                st.session_state.pengali = random.randint(1, 10)
                
                # Hitung kunci jawaban awal
                kunci = (i * st.session_state.pengali) if st.session_state.mode == "perkalian" else (i + st.session_state.pengali)
                st.session_state.pilihan_jawaban = buat_pilihan_ganda(kunci)
                st.session_state.game_started = True
                st.rerun()
                
    st.write("")
    if st.button("⬅️ KEMBALI PILIH MODE", use_container_width=True, key="btn_kembali_mode"):
        st.session_state.mode = None
        st.rerun()

# --- TAMPILAN 3: ARENA BERMAIN ---
else:
    st.markdown(f'<div class="papan-skor">❤️ NYAWA: {"❤️ " * st.session_state.nyawa} | ⭐ SKOR: {st.session_state.skor} PTS</div>', unsafe_allow_html=True)
    
    if st.session_state.nyawa <= 0:
        st.error("🚨 GAME OVER! SISTEM CRASHED. Coba lagi, agen muda! 💪")
        if st.button("KEMBALI KE MENU", use_container_width=True, key="btn_restart"):
            st.session_state.game_started = False
            st.session_state.mode = None
            st.session_state.nyawa = 3
            st.session_state.skor = 0
            st.session_state.feedback = ""
            st.rerun()
            
    else:
        A = st.session_state.angka_tetap
        B = st.session_state.pengali
        
        if st.session_state.mode == "perkalian":
            jawaban_benar = A * B
            tanda_tanya = f"{A} x {B} = ?"
        else:
            jawaban_benar = A + B
            tanda_tanya = f"{A} + {B} = ?"
        
        st.markdown(f'<div class="kotak-soal">BERAPA HASIL DARI:<br>{tanda_tanya}</div>', unsafe_allow_html=True)
        
        if not st.session_state.pilihan_jawaban:
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(jawaban_benar)

        if st.session_state.feedback:
            if st.session_state.tipe_feedback == "success":
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
            st.session_state.feedback = ""

        # Tombol Pilihan Ganda
        col_a, col_b = st.columns(2)
        jawaban_dipilih = None
        
        with col_a:
            if st.button(f"🤖 [ {st.session_state.pilihan_jawaban[0]} ]", use_container_width=True, key="btn_0"):
                jawaban_dipilih = st.session_state.pilihan_jawaban[0]
            if st.button(f"⚡ [ {st.session_state.pilihan_jawaban[1]} ]", use_container_width=True, key="btn_1"):
                jawaban_dipilih = st.session_state.pilihan_jawaban[1]
                
        with col_b:
            if st.button(f"🚀 [ {st.session_state.pilihan_jawaban[2]} ]", use_container_width=True, key="btn_2"):
                jawaban_dipilih = st.session_state.pilihan_jawaban[2]
            if st.button(f"🔮 [ {st.session_state.pilihan_jawaban[3]} ]", use_container_width=True, key="btn_3"):
                jawaban_dipilih = st.session_state.pilihan_jawaban[3]

        if jawaban_dipilih is not None:
            operasi_str = "x" if st.session_state.mode == "perkalian" else "+"
            if jawaban_dipilih == jawaban_benar:
                st.session_state.skor += 10
                st.session_state.feedback = f"🎯 TARGET ACQUIRED! BENAR: {A} {operasi_str} {B} = {jawaban_benar}"
                st.session_state.tipe_feedback = "success"
            else:
                st.session_state.nyawa -= 1
                st.session_state.feedback = f"💥 SYSTEM DAMAGE! KOREKSI: {A} {operasi_str} {B} SEHARUSNYA {jawaban_benar}"
                st.session_state.tipe_feedback = "error"
                
            # Acak soal baru
            angka_baru = random.randint(1, 10)
            while angka_baru == B:
                angka_baru = random.randint(1, 10)
                
            st.session_state.pengali = angka_baru
            kunci_baru = (A * angka_baru) if st.session_state.mode == "perkalian" else (A + angka_baru)
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(kunci_baru)
            
            time.sleep(1.2)
            st.rerun()
                
        st.write("")
        if st.button("⬅️ TERMINATE MISSION (KELUAR)", key="btn_kembali", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.mode = None
            st.session_state.nyawa = 3
            st.session_state.skor = 0
            st.session_state.feedback = ""
            st.rerun()
