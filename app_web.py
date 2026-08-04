import random
import streamlit as st

# Judul Aplikasi
st.title("Latihan Soal Matematika Tanpa Batas")

# Inisialisasi session state untuk skor dan soal
if "score" not in st.session_state:
  st.session_state.score = 0
if "total" not in st.session_state:
  st.session_state.total = 0
if "mode" not in st.session_state:
  st.session_state.mode = "Pertambahan"


# Fungsi membuat soal baru
def generate_question(mode):
  if mode == "Pertambahan":
    n1, n2 = random.randint(1, 50), random.randint(1, 50)
    st.session_state.correct = n1 + n2
    st.session_state.symbol = "+"
  elif mode == "Pengurangan":
    n1, n2 = random.randint(1, 50), random.randint(1, 50)
    if n1 < n2:
      n1, n2 = n2, n1
    st.session_state.correct = n1 - n2
    st.session_state.symbol = "-"
  elif mode == "Perkalian":
    n1, n2 = random.randint(1, 12), random.randint(1, 12)
    st.session_state.correct = n1 * n2
    st.session_state.symbol = "×"

  st.session_state.n1 = n1
  st.session_state.n2 = n2


# Jika soal belum ada, buat baru
if "n1" not in st.session_state:
  generate_question(st.session_state.mode)

# Menu Pilihan Operasi (Radio Button)
mode_baru = st.radio(
    "Pilih Menu:", ["Pertambahan", "Pengurangan", "Perkalian"], horizontal=True
)

# Jika menu diubah, reset skor dan buat soal baru
if mode_baru != st.session_state.mode:
  st.session_state.mode = mode_baru
  st.session_state.score = 0
  st.session_state.total = 0
  generate_question(mode_baru)
  st.rerun()

# Tampilkan Soal
st.markdown(
    f"### Berapakah: {st.session_state.n1} {st.session_state.symbol}"
    f" {st.session_state.n2} ?"
)

# Form Input Jawaban
with st.form(key="form_jawaban", clear_submit=True):
  jawaban_user = st.number_input(
      "Masukkan Jawaban Anda", step=1, format="%d", value=0
  )
  submit = st.form_submit_button("Jawab")

  if submit:
    st.session_state.total += 1
    if jawaban_user == st.session_state.correct:
      st.session_state.score += 1
      st.success("Benar! 🎉")
    else:
      st.error(
          f"Salah! Jawaban yang benar adalah {st.session_state.correct}."
      )
    generate_question(st.session_state.mode)
    st.rerun()

# Tampilkan Skor
st.write(
    f"**Skor:** {st.session_state.score} dari {st.session_state.total} soal"
)
