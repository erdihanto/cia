import random
import streamlit as st

# Judul Aplikasi
st.title("Latihan Soal Matematika Tanpa Batas (Pilihan Ganda)")

# Inisialisasi session state untuk skor dan soal
if "score" not in st.session_state:
  st.session_state.score = 0
if "total" not in st.session_state:
  st.session_state.total = 0
if "mode" not in st.session_state:
  st.session_state.mode = "Pertambahan"


# Fungsi membuat soal baru dan pilihan ganda
def generate_question(mode):
  if mode == "Pertambahan":
    n1, n2 = random.randint(1, 50), random.randint(1, 50)
    correct = n1 + n2
    symbol = "+"
  elif mode == "Pengurangan":
    n1, n2 = random.randint(1, 50), random.randint(1, 50)
    if n1 < n2:
      n1, n2 = n2, n1
    correct = n1 - n2
    symbol = "-"
  elif mode == "Perkalian":
    n1, n2 = random.randint(1, 12), random.randint(1, 12)
    correct = n1 * n2
    symbol = "×"

  # Buat 3 pilihan salah yang mirip/acak
  options = [correct]
  while len(options) < 4:
    # Buat angka pengecoh di sekitar jawaban benar
    offset = random.randint(-10, 10)
    wrong = correct + offset
    if wrong != correct and wrong not in options and wrong >= 0:
      options.append(wrong)

  # Acak posisi pilihan jawaban
  random.shuffle(options)

  st.session_state.n1 = n1
  st.session_state.n2 = n2
  st.session_state.symbol = symbol
  st.session_state.correct = correct
  st.session_state.options = options


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

# Form Pilihan Ganda
with st.form(key="form_pilihan_ganda"):
  # Tampilkan pilihan jawaban dalam bentuk Radio Button
  jawaban_user = st.radio(
      "Pilih jawaban Anda:", st.session_state.options, index=None
  )
  submit = st.form_submit_button("Jawab")

  if submit:
    if jawaban_user is None:
      st.warning("Silakan pilih salah satu jawaban terlebih dahulu!")
    else:
      st.session_state.total += 1
      if jawaban_user == st.session_state.correct:
        st.session_state.score += 1
        st.success("Benar! 🎉")
      else:
        st.error(
            f"Salah! Jawaban yang benar adalah {st.session_state.correct}."
        )

      # Buat soal baru setelah menjawab
      generate_question(st.session_state.mode)
      st.rerun()

# Tampilkan Skor
st.write(
    f"**Skor:** {st.session_state.score} dari {st.session_state.total} soal"
)
