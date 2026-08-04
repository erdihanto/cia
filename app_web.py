import random
import streamlit as st

# Konfigurasi Halaman & Tema Modern
st.set_page_config(
    page_title="MathMaster Pro", page_icon="📐", layout="centered"
)

# Custom CSS untuk tampilan UI/UX yang sangat profesional & modern
st.markdown(
    """
    <style>
    /* Mengubah background utama dan font */
    .main {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Judul Utama */
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e293b;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Kotak Kartu Soal */
    .question-card {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4);
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }

    /* Memaksa semua tombol pilihan ganda memiliki lebar 100% dan ukuran sama */
    div.stButton > button {
        width: 100% !important;
        background-color: #ffffff;
        color: #1e293b;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        font-size: 1.25rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        display: block;
    }
    div.stButton > button:hover {
        background-color: #3b82f6;
        color: #ffffff;
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Desain Sidebar agar lebih bersih dan rapi */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
        padding: 1.5rem 1rem;
    }

    /* Sembunyikan elemen bawaan Streamlit yang mengganggu estetika */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Inisialisasi Session State
if "score" not in st.session_state:
  st.session_state.score = 0
if "total" not in st.session_state:
  st.session_state.total = 0
if "mode" not in st.session_state:
  st.session_state.mode = "Pertambahan"
if "digit" not in st.session_state:
  st.session_state.digit = "1 Digit"
if "feedback" not in st.session_state:
  st.session_state.feedback = None


# Fungsi Generator Soal
def generate_question(mode, digit_str):
  if digit_str == "1 Digit":
    min_val, max_val = 1, 9
  elif digit_str == "2 Digit":
    min_val, max_val = 10, 99
  elif digit_str == "3 Digit":
    min_val, max_val = 100, 999
  elif digit_str == "4 Digit":
    min_val, max_val = 1000, 9999
  else:
    min_val, max_val = 1, 9

  if mode == "Perkalian":
    if digit_str == "2 Digit":
      min_val, max_val = 10, 99
    elif digit_str in ["3 Digit", "4 Digit"]:
      min_val, max_val = 10, 99

  n1 = random.randint(min_val, max_val)
  n2 = random.randint(min_val, max_val)

  if mode == "Pertambahan":
    correct = n1 + n2
    symbol = "+"
  elif mode == "Pengurangan":
    if n1 < n2:
      n1, n2 = n2, n1
    correct = n1 - n2
    symbol = "-"
  elif mode == "Perkalian":
    correct = n1 * n2
    symbol = "×"

  options = [correct]
  while len(options) < 4:
    offset = random.randint(1, max(10, int(correct * 0.2) + 1))
    wrong = correct + random.choice([-offset, offset])
    if wrong != correct and wrong not in options and wrong >= 0:
      options.append(wrong)

  random.shuffle(options)

  st.session_state.n1 = n1
  st.session_state.n2 = n2
  st.session_state.symbol = symbol
  st.session_state.correct = correct
  st.session_state.options = options


if "options" not in st.session_state:
  generate_question(st.session_state.mode, st.session_state.digit)

# Header Aplikasi
st.markdown('<p class="app-title">MathMaster Pro</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Asah kemampuan berhitung cepatmu tanpa'
    " batas</p>",
    unsafe_allow_html=True,
)

# Sidebar Menu Modern (Penyempurnaan Tampilan Menu)
with st.sidebar:
  st.markdown("### 🎛️ Panel Kontrol")
  st.markdown(
      "<p style='font-size: 0.85rem; color: #64748b;'>Sesuaikan parameter"
      " latihan Anda di bawah ini:</p>",
      unsafe_allow_html=True,
  )

  st.markdown("---")
  st.markdown(
      "<p style='font-weight: 600; font-size: 0.9rem; color:"
      " #334155;'>Tingkat Kesulitan (Digit)</p>",
      unsafe_allow_html=True,
  )
  digit_baru = st.pills(
      "Pilih Digit",
      ["1 Digit", "2 Digit", "3 Digit", "4 Digit"],
      default=st.session_state.digit,
      label_visibility="collapsed",
  )

  st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
  st.markdown(
      "<p style='font-weight: 600; font-size: 0.9rem; color:"
      " #334155;'>Operasi Hitung</p>",
      unsafe_allow_html=True,
  )
  mode_baru = st.pills(
      "Pilih Operasi",
      ["Pertambahan", "Pengurangan", "Perkalian"],
      default=st.session_state.mode,
      label_visibility="collapsed",
  )

  # Fallback jika pills kosong saat pertama dimuat
  if not digit_baru:
    digit_baru = st.session_state.digit
  if not mode_baru:
    mode_baru = st.session_state.mode

  st.markdown("---")
  if st.button("🔄 Reset Statistik", use_container_width=True):
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.feedback = None
    generate_question(mode_baru, digit_baru)
    st.rerun()

# Cek perubahan konfigurasi menu
if digit_baru != st.session_state.digit or mode_baru != st.session_state.mode:
  st.session_state.digit = digit_baru
  st.session_state.mode = mode_baru
  st.session_state.score = 0
  st.session_state.total = 0
  st.session_state.feedback = None
  generate_question(mode_baru, digit_baru)
  st.rerun()

# Dashboard Skor (Metrik Profesional)
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric(
    label="Skor Benar", value=st.session_state.score, delta="Poin Aktif"
)
col_m2.metric(label="Total Soal", value=st.session_state.total)
akurasi = (
    int((st.session_state.score / st.session_state.total) * 100)
    if st.session_state.total > 0
    else 0
)
col_m3.metric(label="Akurasi", value=f"{akurasi}%")

st.markdown("---")

# Area Feedback / Warning
if st.session_state.feedback:
  status, pesan = st.session_state.feedback
  if status == "benar":
    st.success(pesan)
  else:
    st.error(pesan)

# Tampilan Kartu Soal Modern
soal_html = (
    f'<div class="question-card">{st.session_state.n1}'
    f" {st.session_state.symbol} {st.session_state.n2} = ?</div>"
)
st.markdown(soal_html, unsafe_allow_html=True)


# Fungsi Logika Jawaban
def jawab(pilihan):
  st.session_state.total += 1
  if pilihan == st.session_state.correct:
    st.session_state.score += 1
    st.session_state.feedback = (
        "benar",
        "Luar biasa! Jawaban Anda sebelumnya **Benar**! 🚀",
    )
  else:
    st.session_state.feedback = (
        "salah",
        f"⚠️ **Kurang Tepat!** Jawaban yang benar untuk soal sebelumnya adalah"
        f" **{st.session_state.correct}**.",
    )
  generate_question(st.session_state.mode, st.session_state.digit)


# Tata Letak Tombol Pilihan Ganda (Grid 2x2 dengan ukuran tombol sama rata)
col1, col2 = st.columns(2)

with col1:
  if st.button(str(st.session_state.options[0]), use_container_width=True):
    jawab(st.session_state.options[0])
    st.rerun()
  if st.button(str(st.session_state.options[1]), use_container_width=True):
    jawab(st.session_state.options[1])
    st.rerun()

with col2:
  if st.button(str(st.session_state.options[2]), use_container_width=True):
    jawab(st.session_state.options[2])
    st.rerun()
  if st.button(str(st.session_state.options[3]), use_container_width=True):
    jawab(st.session_state.options[3])
    st.rerun()
