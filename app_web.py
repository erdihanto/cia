import random
import time

def main():
    print("=======================================")
    print("🎉 SELAMAT DATANG DI GAME PERKALIAN! 🎉")
    print("=======================================")
    print("Halo! Mari belajar perkalian sambil bermain. 😊")
    
    # Pilih mode perkalian
    while True:
        print("\nPilih angka perkalian yang ingin kamu pelajari:")
        print("1. Perkalian 1")
        print("2. Perkalian 2")
        print("3. Perkalian 3")
        print("4. Perkalian 4")
        
        pilihan = input("Masukkan pilihanmu (1-4): ")
        if pilihan in ['1', '2', '3', '4']:
            angka_tetap = int(pilihan)
            break
        else:
            print("❌ Pilihan tidak valid, yuk pilih angka 1 sampai 4!")

    print(f"\n👍 Hebat! Kamu memilih Perkalian {angka_tetap}.")
    print("Kamu punya 3 ❤️ (nyawa). Jawab yang teliti ya!")
    print("Game dimulai dalam 3 detik...")
    time.sleep(3)
    
    # Inisialisasi Game
    skor = 0
    nyawa = 3
    # Membuat daftar angka 1-10 untuk dikalikan secara acak
    daftar_pengali = list(range(1, 11))
    random.shuffle(daftar_pengali)

    # Loop Game
    while nyawa > 0 and len(daftar_pengali) > 0:
        # Ambil satu angka pengali dari daftar
        pengali = daftar_pengali.pop()
        jawaban_benar = angka_tetap * pengali
        
        print("\n---------------------------------------")
        print(f"❤️ Nyawa: {nyawa} | ⭐ Skor: {skor}")
        print(f"Berapa hasil dari: {angka_tetap} x {pengali} ?")
        
        # Validasi input agar game tidak error jika anak salah ketik huruf
        try:
            jawaban_anak = int(input("Jawab: "))
        except ValueError:
            print("⚠️ Oops! Masukkan angka saja ya.")
            daftar_pengali.append(pengali) # Kembalikan soal jika salah input format
            continue

        # Cek jawaban (Sudah diperbaiki)
        if jawaban_anak == jawaban_benar:
            skor += 10
            pesan_hebat = ["Keren banget! ✨", "Betul sekali! 🚀", "Kamu pintar! 🌟", "Luar biasa! 🔥"]
            print(f"✅ {random.choice(pesan_hebat)}")
        else:
            nyawa -= 1
            print(f"❌ Yah, kurang tepat. Yang benar adalah {jawaban_benar}.")
            if nyawa > 0:
                print("Ayo coba lagi di soal berikutnya! 💪")

    # Game Over / Selesai
    print("\n=======================================")
    if nyawa == 0:
        print("GAME OVER 🎮")
        print("Jangan sedih, kamu bisa coba lagi nanti!")
    else:
        print("🎉 SELAMAT! KAMU BERHASIL MENYELESAIKAN SEMUA SOAL! 🎉")
        
    print(f"Skor Akhir Kamu: {skor} ⭐")
    print("Terima kasih sudah bermain! Sampai jumpa lagi. 👋")
    print("=======================================")

if __name__ == "__main__":
    main()
