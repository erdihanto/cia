import random
import time
import streamlit as st

# Konfigurasi Tampilan Halaman
st.set_page_config(page_title="Kuis Penjumlahan Satuan", page_icon="🔢")

st.title("🔢 Kuis Penjumlahan Satuan")
st.caption("Pilih jawaban yang benar. Soal akan otomatis berganti setelah dijawab!")

# Inisialisasi State Skor dan Feedback
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "num1" not in st.session_state:
    st.session_state.num1 = random.randint(0, 9)
    st.session_state.num2 = random.randint(0, 9)
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

# Fungsi untuk Menyiapkan Soal Baru
def generate_next_question():
    st.session_state.num1 = random.randint(0, 9)
    st.session_state.num2 = random.randint(0, 9)

# Tampilkan Skor Saat Ini
st.metric(label="Skor Kamu", value=f"{st.session_state.score} / {st.session_state.total}")

# Tampilkan Notifikasi Hasil dari Soal Sebelumnya (jika ada)
if st.session_state.last_feedback:
    status_type, msg = st.session_state.last_feedback
    if status_type == "success":
        st.success(msg)
    else:
        st.error(msg)

st.divider()

# Tampilkan Soal
num1 = st.session_state.num1
num2 = st.session_state.num2
correct_answer = num1 + num2

st.header(f"{num1} + {num2} = ?")

# Generate Opsi Jawaban
random.seed(num1 * 10 + num2)
wrong_answers = set()
while len(wrong_answers) < 3:
    fake = random.randint(0, 18)
    if fake != correct_answer:
        wrong_answers.add(fake)

options = list(wrong_answers) + [correct_answer]
random.shuffle(options)
random.seed()

# Fungsi yang Dipanggil Saat Jawaban Diklik
def check_answer(user_choice, correct):
    st.session_state.total += 1
    if user_choice == correct:
        st.session_state.score += 1
        st.session_state.last_feedback = ("success", f"🎉 Benar! ({num1} + {num2} = {correct})")
    else:
        st.session_state.last_feedback = ("error", f"❌ Salah! Jawaban ({num1} + {num2}) yang benar adalah {correct}.")
    
    # Langsung ganti ke soal berikutnya
    generate_next_question()

# Tampilkan Tombol Pilihan Jawaban (2x2 grid)
col1, col2 = st.columns(2)
for idx, opt in enumerate(options):
    col = col1 if idx % 2 == 0 else col2
    col.button(
        f"{opt}", 
        key=f"opt_{opt}", 
        use_container_width=True,
        on_click=check_answer,
        args=(opt, correct_answer)
    )
