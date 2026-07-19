import streamlit as st
import random

# Konfigurasi Halaman Browser
st.set_page_config(page_title="KB-TK Kristen Dian Wacana", page_icon="🏫", layout="wide")

# Gaya Tampilan Visual Ceria (CSS Custom)
st.markdown("""
    <style>
    .main { background-color: #E0F2FE; }
    h1 { color: #FF9F1C; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE SISWA ---
if 'database_siswa' not in st.session_state:
    st.session_state.database_siswa = {
        "KB": {"Adit": 0, "Amari": 0, "Levin": 0, "Sienny": 0, "Jesselyn": 0, "Kenzou": 0, "Ralf": 0},
        "TK A": {
            "Kenzie": 0, "Brigitta": 0, "Essy": 0, "Felicia": 0, "Geva": 0, 
            "Greesa": 0, "Laras": 0, "Liam": 0, "Lova": 0, "Nawasena": 0, 
            "Mashal": 0, "Senja": 0, "Viola": 0, "Zio": 0
        },
        "TK B": {
            "Aileen": 0, "Agatha": 0, "Daniel": 0, "Sean": 0, "Elvano": 0, 
            "Betha": 0, "Hiro": 0, "Karen": 0, "Reiga": 0, "Danis": 0, "Yura": 0
        }
    }

if 'status_hadir' not in st.session_state:
    st.session_state.status_hadir = {kelas: {nama: False for nama in siswa} for kelas, siswa in st.session_state.database_siswa.items()}

if 'game_aktif' not in st.session_state:
    st.session_state.game_aktif = None

# --- HEADER APLIKASI ---
st.title("🏫 E-Learning & Absensi: KB-TK Kristen DIAN WACANA")
st.subheader("🌈 Pintar • Berbakti • Ceria")
st.write("---")

# --- LAYOUT DUA KOLOM ---
kolom_kiri, kolom_kanan = st.columns([1, 1.2])

# ==================== PANEL KIRI: ABSENSI ====================
with kolom_kiri:
    st.markdown("### ✨ 1. Pilih Kelas & Nama ✨")
    
    # Pilih Kelas
    kelas = st.selectbox("Pilih Kelasmu:", ["KB", "TK A", "TK B"])
    info_usia = {"KB": "Usia 3-4 Tahun", "TK A": "Usia 4-5 Tahun", "TK B": "Usia 5-6 Tahun"}
    st.info(f"👶 {info_usia[kelas]}")
    
    # Urutkan nama siswa
    daftar_nama = sorted(list(st.session_state.database_siswa[kelas].keys()))
    
    # Pilih Nama
    nama_terpilih = st.selectbox("Siapa Namamu?", ["-- Pilih Nama --"] + daftar_nama)
    
    if nama_terpilih != "-- Pilih Nama --":
        hadir = st.session_state.status_hadir[kelas][nama_terpilih]
        bintang = st.session_state.database_siswa[kelas][nama_terpilih]
        
        if hadir:
            st.success(f"🥰 Halo {nama_terpilih}! Kamu sudah hadir hari ini. Bintangmu: {bintang} ⭐")
        else:
            st.warning(f"🙂 Ayo absen dulu, {nama_terpilih}!")
            if st.button("✋ SAYA HADIR! 🎈", type="primary"):
                st.session_state.status_hadir[kelas][nama_terpilih] = True
                st.rerun()

# ==================== PANEL KANAN: GAME ZONA BERMAIN ====================
with kolom_kanan:
    st.markdown(f"### 🎮 ZONA BERMAIN KELAS {kelas}")
    
    if nama_terpilih == "-- Pilih Nama --" or not st.session_state.status_hadir[kelas][nama_terpilih]:
        st.info("Silakan pilih namamu dan klik tombol **SAYA HADIR!** di sebelah kiri terlebih dahulu untuk bermain! 😊")
    else:
        # Pilihan game berdasarkan kategori
        def get_game(kategori):
            if kategori == "KB":
                return random.choice([
                    ("🍎 🍎", "Ada berapa jumlah buah apel merah di atas?", ["1", "2", "3"], "2"),
                    ("🐶", "Suara hewan apakah di atas?", ["Guk-Guk 🐕", "Meong 🐈", "Kwek-Kwek 🦆"], "Guk-Guk 🐕"),
                    ("❤️", "Warna apakah balon hati ini?", ["Merah ❤️", "Biru 💙", "Kuning 💛"], "Merah ❤️")
                ])
            elif kategori == "TK A":
                return random.choice([
                    ("🐘 ... 🐁", "Siapa yang badannya LEBIH BESAR?", ["Gajah 🐘", "Tikus 🐁", "Semut 🐜"], "Gajah 🐘"),
                    ("A, B, _, D", "Huruf apa yang kosong di atas?", ["C", "M", "Q"], "C"),
                    ("🚗 🚗 🚕 🚗", "Mobil ke berapa yang warnanya BERBEDA?", ["Ke-1", "Ke-2", "Ke-3"], "Ke-3")
                ])
            else: # TK B
                return random.choice([
                    ("3 + 2 = ?", "Berapakah hasil penjumlahan di atas?", ["4", "5", "6"], "5"),
                    ("B _ N D E R A", "Lengkapi huruf vokal yang hilang!", ["A", "E", "O"], "E"),
                    ("✈️", "Kendaraan di atas berjalan di mana?", ["Darat 🛣️", "Laut 🌊", "Udara ☁️"], "Udara ☁️")
                ])

        if st.button("🎲 MAIN / ACAK GAME BARU", type="secondary"):
            st.session_state.game_aktif = get_game(kelas)
            if 'jawaban_terjawab' in st.session_state:
                del st.session_state.jawaban_terjawab

        # Menampilkan Game jika sudah di-klik
        if st.session_state.game_aktif:
            visual, pertanyaan, opsi, jawaban_benar = st.session_state.game_aktif
            
            # Box Visual Game besar
            st.markdown(f"<h1 style='text-align: center; font-size: 80px; background-color: #FFF9C4; border-radius: 15px; padding: 20px;'>{visual}</h1>", unsafe_allow_html=True)
            st.markdown(f"#### {pertanyaan}")
            
            # Tombol Pilihan Jawaban
            kol_opsi = st.columns(len(opsi))
            for i, alternatif in enumerate(opsi):
                with kol_opsi[i]:
                    if st.button(alternatif, key=f"btn_{alternatif}"):
                        st.session_state.jawaban_terjawab = alternatif

            # Cek Jawaban
            if 'jawaban_terjawab' in st.session_state:
                if st.session_state.jawaban_terjawab == jawaban_benar:
                    st.balloons()
                    st.success(f"🏆 HEBAT! BENAR! Skor Bintang {nama_terpilih} bertambah! 🎉")
                    st.session_state.database_siswa[kelas][nama_terpilih] += 1
                    st.session_state.game_aktif = None # Reset game setelah benar
                else:
                    st.error("💪 Coba lagi ya! Kamu pasti bisa!")