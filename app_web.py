import random
import streamlit as st

# Konfigurasi Tampilan Halaman
st.set_page_config(page_title="Kuis Penjumlahan Satuan", page_icon="🔢")

st.title("🔢 Kuis Penjumlahan Satuan")
st.write("Jawab soal penjumlahan berikut. Soal tidak terbatas dan acak!")

# Inisialisasi state untuk menyimpan skor & status
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "num1" not in st.session_state:
    st.session_state.num1 = random.randint(0, 9)
    st.session_state.num2 = random.randint(0, 9)
    st.session_state.answered = False
    st.session_state.feedback = ""

# Fungsi untuk membuat soal baru
def generate_new_question():
    st.session_state.num1 = random.randint(0, 9)
    st.session_state.num2 = random.randint(0, 9)
    st.session_state.answered = False
    st.session_state.feedback = ""

correct_answer = st.session_state.num1 + st.session_state.num2

# Tampilkan Skor
st.metric(label="Skor Kamu", value=f"{st.session_state.score} / {st.session_state.total}")
st.divider()

# Tampilkan Soal
st.header(f"{st.session_state.num1} + {st.session_state.num2} = ?")

# Buat Opsi Pilihan Ganda (1 jawaban benar, 3 salah)
# Gunakan seed berdasarkan angka agar pilihan tidak teracak ulang setiap klik
random.seed(st.session_state.num1 * 10 + st.session_state.num2)
wrong_answers = set()
while len(wrong_answers) < 3:
    fake = random.randint(0, 18)
    if fake != correct_answer:
        wrong_answers.add(fake)

options = list(wrong_answers) + [correct_answer]
random.shuffle(options)
random.seed() # Reset seed

# Tampilkan Tombol Pilihan Jawaban (2x2 grid)
col1, col2 = st.columns(2)
for idx, opt in enumerate(options):
    col = col1 if idx % 2 == 0 else col2
    if col.button(f"{opt}", key=f"opt_{opt}", use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if opt == correct_answer:
            st.session_state.score += 1
            st.session_state.feedback = ("success", "🎉 Benar! Bagus sekali!")
        else:
            st.session_state.feedback = ("error", f"❌ Salah! Jawaban yang benar adalah {correct_answer}.")
        st.rerun()

# Tampilkan Feedback Hasil
if st.session_state.feedback:
    status_type, msg = st.session_state.feedback
    if status_type == "success":
        st.success(msg)
    else:
        st.error(msg)
    
    st.button("Soal Berikutnya ➔", on_click=generate_new_question, type="primary")
