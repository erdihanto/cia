import streamlit as st
import random

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Game Perkalian Anak", page_icon="🎮", layout="centered")

# 2. Judul Game
st.title("🎉 GAME PERKALIAN SERU! 🎉")
st.write("Halo! Mari belajar perkalian sambil bermain. Pilih jawaban yang benar ya! 😊")

# 3. Inisialisasi State / Penyimpanan Data Game
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

# Fungsi untuk membuat pilihan ganda acak
def buat_pilihan_ganda(kunci_jawaban):
    pilihan = {kunci_jawaban}
    # Cari 3 angka acak lain di sekitar jawaban yang benar agar anak tetap tertantang
    while len(pilihan) < 4:
        salah = kunci_jawaban + random.randint(-5, 5)
        if salah > 0 and salah != kunci_jawaban:
            pilihan.add(salah)
    
    list_pilihan = list(pilihan)
    random.shuffle(list_pilihan)
    return list_pilihan

# --- TAMPILAN 1: MENU UTAMA (PILIH PERKALIAN 2-4) ---
if not st.session_state.game_started:
    st.subheader("Pilih angka perkalian yang ingin kamu pelajari:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔢 Perkalian 2", use_container_width=True):
            st.session_state.angka_tetap = 2
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(2 * st.session_state.pengali)
            st.session_state.game_started = True
            st.rerun()
    with col2:
        if st.button("🔢 Perkalian 3", use_container_width=True):
            st.session_state.angka_tetap = 3
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(3 * st.session_state.pengali)
            st.session_state.game_started = True
            st.rerun()
    with col3:
        if st.button("🔢 Perkalian 4", use_container_width=True):
            st.session_state.angka_tetap = 4
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(4 * st.session_state.pengali)
            st.session_state.game_started = True
            st.rerun()

# --- TAMPILAN 2: ARENA BERMAIN (PILIHAN GANDA) ---
else:
    # Tampilkan Scoreboard
    st.markdown(f"### ❤️ Nyawa: {'❤️ ' * st.session_state.nyawa} | ⭐ Skor: {st.session_state.skor}")
    st.markdown("---")
    
    # Cek status kalah
    if st.session_state.nyawa <= 0:
        st.error("🎮 GAME OVER! Jangan sedih ya, yuk coba lagi! 💪")
        if st.button("Main Lagi 🔄", use_container_width=True):
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
        
        # Jika pilihan jawaban kosong (pengaman sistem), buat baru
        if not st.session_state.pilihan_jawaban:
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(jawaban_benar)

        # Tampilkan 4 Tombol Pilihan Ganda
        st.write("Pilih salah satu jawaban di bawah ini:")
        col_a, col_b = st.columns(2)
        
        jawaban_dipilih = None
        
        with col_a:
            if st.button(f"🅰️  {st.session_state.pilihan_jawaban[0]}", use_container_width=True):
                jawaban_dipilih = st.session_state.pilihan_jawaban[0]
            if st.button(f"🅱️  {st.session_state.pilihan_jawaban[1]}", use_container_width=True):
                jawaban_dipilih = st.session_state.pilihan_jawaban[1]
                
        with col_b:
            if st.button(f"🆃  {st.session_state.pilihan_jawaban[2]}", use_container_width=True):
                jawaban_dipilih = st.session_state.pilihan_jawaban[2]
            if st.button(f"🅳  {st.session_state.pilihan_jawaban[3]}", use_container_width=True):
                jawaban_dipilih = st.session_state.pilihan_jawaban[3]

        # Proses jawaban jika salah satu tombol diklik
        if jawaban_dipilih is not None:
            if jawaban_dipilih == jawaban_benar:
                st.session_state.skor += 10
                pesan_hebat = ["Keren banget! ✨", "Betul sekali! 🚀", "Kamu pintar! 🌟", "Luar biasa! 🔥"]
                st.session_state.feedback = f"✅ {random.choice(pesan_hebat)} ({A} x {B} = {jawaban_benar})"
                st.session_state.tipe_feedback = "success"
            else:
                st.session_state.nyawa -= 1
                st.session_state.feedback = f"❌ Yah, kurang tepat. {A} x {B} yang benar adalah {jawaban_benar}."
                st.session_state.tipe_feedback = "error"
                
            # Siapkan soal dan pilihan ganda baru untuk ronde selanjutnya
            st.session_state.pengali = random.randint(1, 10)
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(A * st.session_state.pengali)
            st.rerun()
            
        # Tampilkan Pesan Benar/Salah dari soal sebelumnya
        if st.session_state.feedback:
            if st.session_state.tipe_feedback == "success":
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
                
        # Tombol kembali ke menu utama
        st.write("")
        if st.button("⬅️ Kembali ke Menu Utama"):
            st.session_state.game_started = False
            st.session_state.nyawa = 3
            st.session_state.skor = 0
            st.session_state.feedback = ""
            st.rerun()
