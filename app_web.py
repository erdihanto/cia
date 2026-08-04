import random
import streamlit as st

# Judul Aplikasi
st.title("Latihan Soal Matematika Bertingkat")

# Inisialisasi session state secara lengkap di awal
if "score" not in st.session_state:
  st.session_state.score = 0
if "total" not in st.session_state:
  st.session_state.total = 0
if "mode" not in st.session_state:
  st.session_state.mode = "Pertambahan"
if "digit" not in st.session_state:
  st.session_state.digit = "1 Digit"


# Fungsi membuat soal baru dan pilihan ganda berdasarkan digit dan mode
def generate_question(mode, digit_str):
  # Tentukan rentang angka berdasarkan pilihan digit
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

  # Khusus perkalian, batasan digit bisa disesuaikan agar tidak terlalu besar
  if mode == "Perkalian":
    if digit_str == "2 Digit":
      min_val, max_val = 10, 99
    elif digit_str == "3 Digit" or digit_str == "4 Digit":
      # Batasi maks digit untuk perkalian agar pilihan ganda tidak terlalu ekstrem
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

  # Buat 3 pilihan salah di sekitar jawaban benar
  options = [correct]
  while len(options) < 4:
    # Rentang pengecoh disesuaikan dengan besarnya jawaban
    offset = random.randint(1, max(10, int(correct * 0.2) + 1))
    wrong = correct + random.choice([-offset, offset])
    if wrong != correct and wrong not in options and wrong >= 0:
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
  generate_question(st.session_state.mode, st.session_state.digit)

# Menu Pilihan Digit Angka
digit_baru = st.selectbox(
    "Pilih Jumlah Digit:", ["1 Digit", "2 Digit", "3 Digit", "4 Digit"]
)

# Menu Pilihan Operasi
mode_baru = st.radio(
    "Pilih Operasi:", ["Pertambahan", "Pengurangan", "Perkalian"], horizontal=True
)

# Jika menu digit atau operasi diubah, reset skor dan buat soal baru
if digit_baru != st.session_state.digit or mode_baru != st.session_state.mode:
  st.session_state.digit = digit_baru
  st.session_state.mode = mode_baru
  st.session_state.score = 0
  st.session_state.total = 0
  generate_question(mode_baru, digit_baru)
  st.rerun()

# Tampilkan Soal
st.markdown("---")
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
  generate_question(st.session_state.mode, st.session_state.digit)


# Tampilkan Tombol Pilihan Ganda (2 kolom)
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
st.markdown("---")
st.write(
    f"**Skor:** {st.session_state.score} dari {st.session_state.total} soal"
)
