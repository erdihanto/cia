import streamlit as st
import random
import time

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
            st.session_state.pengali = random.randint(1, 10)  # Soal diacak pertama kali
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(2 * st.session_state.pengali)
            st.session_state.game_started = True
            st.rerun()
    with col2:
        if st.button("🔢 Perkalian 3", use_container_width=True):
            st.session_state.angka_tetap = 3
            st.session_state.pengali = random.randint(1, 10)  # Soal diacak pertama kali
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(3 * st.session_state.pengali)
            st.session_state.game_started = True
            st.rerun()
    with col3:
        if st.button("🔢 Perkalian 4", use_container_width=True):
            st.session_state.angka_tetap = 4
            st.session_state.pengali = random.randint(1, 10)  # Soal diacak pertama kali
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
        # Ambil data soal saat ini
        A = st.session_state.angka_tetap
        B = st.session_state.pengali
        jawaban_benar = A * B
        
        # Tampilkan Soal
        st.info(f"### Berapa hasil dari:  **{A}  x  {B}**  ?", icon="🧮")
        
        # Jika pilihan jawaban kosong, buat baru
        if not st.session_state.pilihan_jawaban:
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(jawaban_benar)

        # Tampilkan Teks Feedback dari Soal Sebelumnya (Jika ada)
        if st.session_state.feedback:
            if st.session_state.tipe_feedback == "success":
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
            # Hapus feedback setelah ditampilkan agar tidak muncul terus di soal berikutnya
            st.session_state.feedback = ""

        # Tampilkan 4 Tombol Pilihan Ganda
        st.write("Pilih salah satu jawaban di bawah ini:")
        col_a, col_b = st.columns(2)
        
        jawaban_dipilih = None
        
        with col_a:
            if st.button(f"🅰️  {st.session_state.pilihan_jawaban[0]}", use_container_width=True, key="btn_0"):
                jawaban_dipilih = st.session_state.pilihan_jawaban[0]
            if st.button(f"🅱️  {st.session_state.pilihan_jawaban[1]}", use_container_width=True, key="btn_1"):
                jawaban_dipilih = st.session_state.pilihan_jawaban[1]
                
        with col_b:
            if st.button(f"🅲  {st.session_state.pilihan_jawaban[2]}", use_container_width=True, key="btn_2"):
                jawaban_dipilih = st.session_state.pilihan_jawaban[2]
            if st.button(f"🅳  {st.session_state.pilihan_jawaban[3]}", use_container_width=True, key="btn_3"):
                jawaban_dipilih = st.session_state.pilihan_jawaban[3]

        # Proses jawaban otomatis saat tombol diklik
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
                
            # --- OTOMATIS ACAK SOAL BARU ---
            # Cari angka pengali baru (1-10) secara acak yang berbeda dari soal barusan
            angka_baru = random.randint(1, 10)
            while angka_baru == B:
                angka_baru = random.randint(1, 10)
                
            st.session_state.pengali = angka_baru
            st.session_state.pilihan_jawaban = buat_pilihan_ganda(A * st.session_state.pengali)
            
            # Beri jeda 1.5 detik agar anak bisa melihat jawaban mereka benar/salah, lalu refresh halaman otomatis
            time.sleep(1.5)
            st.rerun()
                
        # Tombol kembali ke menu utama
        st.write("")
        if st.button("⬅️ Kembali ke Menu Utama", key="btn_kembali"):
            st.session_state.game_started = False
            st.session_state.nyawa = 3
            st.session_state.skor = 0
            st.session_state.feedback = ""
            st.rerun()
