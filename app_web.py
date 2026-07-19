import streamlit as st
import random
import time

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="GAME PERKALIAN CYBER", page_icon="🎮", layout="centered")

# 2. Gaya Desain Custom CSS (Retro Arcade / Neon Cyberpunk)
st.markdown("""
    <style>
    /* Mengubah latar belakang seluruh aplikasi menjadi gelap gulita */
    .stApp {
        background-color: #0d0e15;
        color: #00ff66;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Judul Utama Bergaya Neon */
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
    
    /* Kotak Soal & Informasi */
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
    
    /* Papan Skor */
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
    
    /* Kustomisasi Tombol Streamlit agar Berwarna Warni */
    div.stButton > button {
        background-color: #1a1c28 !important;
        color: #00ff66 !important;
        border: 2px solid #00ff66 !important;
        box-shadow: 0 0 8px #00ff66 !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        padding: 15px 0px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #00ff66 !important;
        color: #000000 !important;
        box-shadow: 0 0 20px #00ff66 !important;
        transform: scale(1.03);
    }
    
    /* Tombol Menu khusus */
    .stButton button[key^="menu_"] {
        border: 2px solid #ff0055 !important;
        color: #ff0055 !important;
        box-shadow: 0 0 8px #ff0055 !important;
    }
    .stButton button[key^="menu_"]:hover {
        background-color: #ff0055 !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px #ff0055 !important;
    }
    
    /* Menyembunyikan elemen bawaan Streamlit yang mengganggu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Judul Atas
st.markdown('<div class="judul-neon">⚡ MULTIPLIER ARCADE ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-judul">> SYSTEM READY: PILIH JAWABAN YANG TEPAT!</div>', unsafe_allow_html=True)

# 4. Inisialisasi State / Data Game
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'skor' not in st.session_state:
    st.session_state.skor = 0
if 'nyawa' not in st.session_state:
    st.session_state.nyawa = 3
if 'angka_tetap' not in st.session_state:
    st.session_state.angka_tetap = 2
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
        salah = kunci_jawaban + random.randint(-5, 5)
        if salah > 0 and salah != kunci_jawaban:
            pilihan.add(salah)
    list_pilihan = list(pilihan)
    random.shuffle(list_pilihan)
    return list_pilihan

# --- TAMPILAN 1: MENU UTAMA ---
if not st.session_state.game_started:
    st.markdown("<h3 style='text-align:center; color:#fff;'>[ PILIH MODE MISI PERKALIAN ]</h3>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔴 PERKALIAN 2", use_container_width=True, key="menu_2"):
            st.session_state.angka_tetap = 2
            st.session_state.pengali = random.randint(1, 10)
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(2 * st.session_state.pengali)
            st.session_state.game_started = True
            st.rerun()
    with col2:
        if st.button("🔵 PERKALIAN 3", use_container_width=True, key="menu_3"):
            st.session_state.angka_tetap = 3
            st.session_state.pengali = random.randint(1, 10)
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(3 * st.session_state.pengali)
            st.session_state.game_started = True
            st.rerun()
    with col3:
        if st.button("🟢 PERKALIAN 4", use_container_width=True, key="menu_4"):
            st.session_state.angka_tetap = 4
            st.session_state.pengali = random.randint(1, 10)
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(4 * st.session_state.pengali)
            st.session_state.game_started = True
            st.rerun()

# --- TAMPILAN 2: ARENA BERMAIN ---
else:
    # Status Bar Atas
    st.markdown(f'<div class="papan-skor">❤️ NYAWA: {"❤️ " * st.session_state.nyawa} | ⭐ SKOR: {st.session_state.skor} PTS</div>', unsafe_allow_html=True)
    
    # Cek Game Over
    if st.session_state.nyawa <= 0:
        st.error("🚨 GAME OVER! SISTEM CRASHED. Coba lagi, agen muda! 💪")
        if st.button("KEMBALI KE MENU", use_container_width=True, key="btn_restart"):
            st.session_state.game_started = False
            st.session_state.nyawa = 3
            st.session_state.skor = 0
            st.session_state.feedback = ""
            st.rerun()
            
    else:
        A = st.session_state.angka_tetap
        B = st.session_state.pengali
        jawaban_benar = A * B
        
        # Tampilkan Kotak Soal Futuristik
        st.markdown(f'<div class="kotak-soal">BERAPA HASIL DARI:<br>{A} x {B} = ?</div>', unsafe_allow_html=True)
        
        if not st.session_state.pilihan_jawaban:
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(jawaban_benar)

        # Tampilkan Teks Koreksi Jawaban Sebelumnya (jika ada)
        if st.session_state.feedback:
            if st.session_state.tipe_feedback == "success":
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
            st.session_state.feedback = ""

        # Tombol Pilihan Ganda bergaya Arcade Neon
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

        # Logika Pengecekan & Pengacakan Otomatis
        if jawaban_dipilih is not None:
            if jawaban_dipilih == jawaban_benar:
                st.session_state.skor += 10
                st.session_state.feedback = f"🎯 TARGET ACQUIRED! BENAR: {A} x {B} = {jawaban_benar}"
                st.session_state.tipe_feedback = "success"
            else:
                st.session_state.nyawa -= 1
                st.session_state.feedback = f"💥 SYSTEM DAMAGE! KOREKSI: {A} x {B} SEHARUSNYA {jawaban_benar}"
                st.session_state.tipe_feedback = "error"
                
            # Otomatis acak soal baru langsung
            angka_baru = random.randint(1, 10)
            while angka_baru == B:
                angka_baru = random.randint(1, 10)
                
            st.session_state.pengali = angka_baru
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(A * st.session_state.pengali)
            
            time.sleep(1.2)
            st.rerun()
                
        # Tombol Keluar / Kembali
        st.write("")
        if st.button("⬅️ TERMINATE MISSION (KELUAR)", key="menu_keluar", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.nyawa = 3
            st.session_state.skor = 0
            st.session_state.feedback = ""
            st.rerun()
