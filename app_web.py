import random
import streamlit as st

# Judul Aplikasi
st.title("Latihan Soal Matematika (1 - 10)")

# Inisialisasi session state secara lengkap di awal
if "score" not in st.session_state:
  st.session_state.score = 0
if "total" not in st.session_state:
  st.session_state.total = 0
if "mode" not in st.session_state:
  st.session_state.mode = "Pertambahan"


# Fungsi membuat soal baru dan pilihan ganda (Angka 1 - 10)
def generate_question(mode):
  if mode == "Pertambahan":
    n1, n2 = random.randint(1, 10), random.randint(1, 10)
    correct = n1 + n2
    symbol = "+"
  elif mode == "Pengurangan":
    n1, n2 = random.randint(1, 10), random.randint(1, 10)
    if n1 < n2:
      n1, n2 = n2, n1
    correct = n1 - n2
    symbol = "-"
  elif mode == "Perkalian":
    n1, n2 = random.randint(1, 10), random.randint(1, 10)
    correct = n1 * n2
    symbol = "×"

  # Buat 3 pilihan salah yang unik di sekitar angka 1-20
  options = [correct]
  while len(options) < 4:
    wrong = random.randint(1, 20)
    if wrong != correct and wrong not in options:
      options.append(wrong)

  # Acak posisi pilihan jawaban
  random.shuffle(options)

  st.session_state.n1 = n1
  st.session_state.n2 = n2
  st.session_state.symbol = symbol
  st.session_state.correct = correct
  st.session_state.options = options


# Pastikan soal digenerate jika belum ada
if "options" not in st.session_state:
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
st.write("Silakan klik salah satu tombol pilihan jawaban di bawah:")

# Fungsi callback saat tombol pilihan diklik
def jawab(pilihan):
  st.session_state.total += 1
  if pilihan == st.session_state.correct:
    st.session_state.score += 1
    st.toast("Benar! 🎉", icon="✅")
  else:
    st.toast(
        f"Salah! Jawaban yang benar adalah {st.session_state.correct}.",
        icon="❌",
    )
  generate_question(st.session_state.mode)


# Tampilkan Tombol Pilihan Ganda (2 kolom agar rapi)
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

# Tampilkan Skor
st.write("")
st.write(
    f"**Skor:** {st.session_state.score} dari {st.session_state.total} soal"
)
