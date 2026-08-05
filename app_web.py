import random
import streamlit as st

# Konfigurasi Halaman & Tema Modern
st.set_page_config(
    page_title="MathMaster Pro", page_icon="✨", layout="centered"
)

# Custom CSS & Integrasi Web Speech API
st.markdown(
    """
    <style>
    .main {
        background-color: #faf5ff;
        font-family: 'Inter', sans-serif;
    }
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #4c1d95;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        font-size: 1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .question-card {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.5);
        margin-bottom: 1.5rem;
        letter-spacing: 2px;
    }
    div.stButton > button {
        width: 100% !important;
        background-color: #ffffff;
        color: #374151;
        border: 2px solid #e5e7eb;
        border-radius: 14px;
        padding: 0.9rem 1rem;
        font-size: 1.25rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        display: block;
    }
    div.stButton > button:hover {
        background-color: #f5f3ff;
        color: #6d28d9;
        border-color: #8b5cf6;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -4px rgba(139, 92, 246, 0.25);
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #f3f4f6;
        padding: 1.5rem 1rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)


# Fungsi untuk memutar suara manusia via JavaScript Browser
def play_natural_voice(text):
    js_code = f"""
    <script>
    function speakText() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            let utterance = new SpeechSynthesisUtterance("{text}");
            utterance.lang = 'id-ID';
            utterance.rate = 0.95;
            utterance.pitch = 1.0;
            
            let voices = window.speechSynthesis.getVoices();
            let indonesianVoice = voices.find(voice => voice.lang === 'id-ID' || voice.lang === 'id_ID');
            if (indonesianVoice) {{
                utterance.voice = indonesianVoice;
            }}
            
            window.speechSynthesis.speak(utterance);
        }}
    }}
    speakText();
    </script>
    """
    st.components.v1.html(js_code, height=0)


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
if "teks_suara" not in st.session_state:
    st.session_state.teks_suara = "Berapakah soal matematika Anda?"


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
        if digit_str in ["2 Digit", "3 Digit", "4 Digit"]:
            min_val, max_val = 10, 99

    n1 = random.randint(min_val, max_val)
    n2 = random.randint(min_val, max_val)

    if mode == "Pertambahan":
        correct = n1 + n2
        symbol_text = " ditambah "
        symbol_display = "+"
    elif mode == "Pengurangan":
        if n1 < n2:
            n1, n2 = n2, n1
        correct = n1 - n2
        symbol_text = " dikurangi "
        symbol_display = "-"
    elif mode == "Perkalian":
        correct = n1 * n2
        symbol_text = " dikali "
        symbol_display = "×"

    options = [correct]
    while len(options) < 4:
        offset = random.randint(1, max(10, int(correct * 0.2) + 1))
        wrong = correct + random.choice([-offset, offset])
        if wrong != correct and wrong not in options and wrong >= 0:
            options.append(wrong)

    random.shuffle(options)

    st.session_state.n1 = n1
    st.session_state.n2 = n2
    st.session_state.symbol = symbol_display
    st.session_state.correct = correct
    st.session_state.options = options
    st.session_state.teks_suara = f"Berapakah {n1} {symbol_text} {n2}?"


if "options" not in st.session_state:
    generate_question(st.session_state.mode, st.session_state.digit)

# Header Aplikasi
st.markdown('<p class="app-title">✨ MathMaster Pro ✨</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Latihan matematika interaktif dengan opsi audio suara</p>',
    unsafe_allow_html=True,
)

# Sidebar Menu Pengaturan
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan Latihan")
    st.markdown("---")

    digit_options = ["1 Digit", "2 Digit", "3 Digit", "4 Digit"]
    digit_index = (
        digit_options.index(st.session_state.digit)
        if st.session_state.digit in digit_options
        else 0
    )
    digit_baru = st.selectbox(
        "Pilih Tingkat Kesulitan:", digit_options, index=digit_index
    )

    mode_options = ["Pertambahan", "Pengurangan", "Perkalian"]
    mode_index = (
        mode_options.index(st.session_state.mode)
        if st.session_state.mode in mode_options
        else 0
    )
    mode_baru = st.selectbox(
        "Pilih Operasi Hitung:", mode_options, index=mode_index
    )

    st.markdown("---")
    st.markdown("### 🔊 Pengaturan Suara")
    gunakan_audio = st.toggle("Gunakan Audio Suara", value=True)

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

# Dashboard Skor
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

# Tampilan Kartu Soal
soal_html = f'<div class="question-card">{st.session_state.n1} {st.session_state.symbol} {st.session_state.n2} = ?</div>'
st.markdown(soal_html, unsafe_allow_html=True)

# Tampilan kontrol audio
if gunakan_audio:
    col_suara1, col_suara2, col_suara3 = st.columns([1, 2, 1])
    with col_suara2:
        if st.button("🔊 Putar Ulang Suara Soal", use_container_width=True):
            play_natural_voice(st.session_state.teks_suara)

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)


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
            f"⚠️ **Kurang Tepat!** Jawaban yang benar adalah **{st.session_state.correct}**.",
        )
    generate_question(st.session_state.mode, st.session_state.digit)


# Tata Letak Tombol Pilihan Ganda
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
