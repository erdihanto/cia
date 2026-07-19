import streamlit as st
import random

# 1. Konfigurasi Halaman (Harus berada di paling atas kode)
st.set_page_config(page_title="Game Perkalian Anak", page_icon="🎮", layout="centered")

# 2. Judul Game
st.title("🎉 GAME PERKALIAN SERU! 🎉")
st.write("Halo! Mari belajar perkalian sambil bermain. 😊")

# 3. Inisialisasi State / Penyimpanan Data Game
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'skor' not in st.session_state:
    st.session_state.skor = 0
if 'nyawa' not in st.session_state:
    st.session_state.nyawa = 3
if 'angka_tetap' not in st.session_state:
    st.session_state.angka_tetap = 1
if 'pengali' not in st.session_state:
    st.session_state.pengali = random.randint(1, 10)
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'tipe_feedback' not in st.session_state:
    st.session_state.tipe_feedback = "info"

# --- TAMPILAN 1: MENU UTAMA (PILIH PERKALIAN) ---
if not st.session_state.game_started:
    st.subheader("Pilih angka perkalian yang ingin kamu pelajari:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔢 Perkalian 1", use_container_width=True):
            st.session_state.angka_tetap = 1
            st.session_state.game_started = True
            st.rerun()
    with col2:
        if st.button("🔢 Perkalian 2", use_container_width=True):
            st.session_state.angka_tetap = 2
            st.session_state.game_started = True
            st.rerun()
    with col3:
        if st.button("🔢 Perkalian 3", use_container_width=True):
            st.session_state.angka_tetap = 3
            st.session_state.game_started = True
            st.rerun()
    with col4:
        if st.button("🔢 Perkalian 4", use_container_width=True):
            st.session_state.angka_tetap = 4
            st.session_state.game_started = True
            st.rerun()

# --- TAMPILAN 2: ARENA BERMAIN ---
else:
    # Tampilkan Scoreboard sederhana
    st.markdown(f"### ❤️ Nyawa: {st.session_state.nyawa} | ⭐ Skor: {st.session_state.skor}")
    st.markdown("---")
    
    # Cek status kalah
    if st.session_state.nyawa <= 0:
        st.error("🎮 GAME OVER! Jangan sedih ya, yuk coba lagi! 💪")
        if st.button("Main Lagi 🔄"):
            st.session_state.game_started = False
            st.session_state.nyawa = 3
            st.session_state.skor = 0
            st.session_state.feedback = ""
            st.rerun()
            
    else:
        # Tampilkan Soal
        A = st.session_state.angka_tetap
        B = st.session_state.pengali
        jawaban_benar = A * B
        
        st.info(f"### Berapa hasil dari:  **{A}  x  {B}**  ?", icon="🧮")
        
        # Input Jawaban
        jawaban_anak = st.number_input("Tulis jawabanmu di sini:", min_value=0, max_value=100, value=0, step=1)
        
        if st.button("Kirim Jawaban 🚀", use_container_width=True):
            if jawaban_anak == jawaban_benar:
                st.session_state.skor += 10
                pesan_hebat = ["Keren banget! ✨", "Betul sekali! 🚀", "Kamu pintar! 🌟", "Luar biasa! 🔥"]
                st.session_state.feedback = f"✅ {random.choice(pesan_hebat)} ({A} x {B} = {jawaban_benar})"
                st.session_state.tipe_feedback = "success"
            else:
                st.session_state.nyawa -= 1
                st.session_state.feedback = f"❌ Yah, kurang tepat. {A} x {B} yang benar adalah {jawaban_benar}."
                st.session_state.tipe_feedback = "error"
                
            # Acak angka baru untuk soal berikutnya
            st.session_state.pengali = random.randint(1, 10)
            st.rerun()
            
        # Tampilkan Pesan Benar/Salah dari soal sebelumnya
        if st.session_state.feedback:
            if st.session_state.tipe_feedback == "success":
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
                
        st.write("")
        if st.button("⬅️ Kembali ke Menu Utama"):
            st.session_state.game_started = False
            st.session_state.nyawa = 3
            st.session_state.skor = 0
            st.session_state.feedback = ""
            st.rerun()
