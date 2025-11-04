import csv
import sys
from modules import admin, dosen, mahasiswa, utils

def header():
    print("=" * 60)
    print("  🧩 SINTAK - Sistem Informasi Nilai, Tugas, dan Kehadiran (CLI)")
    print("=" * 60)

def login():
    header()
    print("[1] Login")
    print("[2] Register (Mahasiswa)")
    print("[3] Keluar")
    pilih = input("Pilih: ").strip()
    if pilih == '1':
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        user = utils.find_user(username, password)
        if user:
            print(f"\n✅ Login berhasil: {username} ({user['role']})\n")
            if user['role'] == 'admin':
                admin.menu_admin(user)
            elif user['role'] == 'dosen':
                dosen.menu_dosen(user)
            elif user['role'] == 'mahasiswa':
                mahasiswa.menu_mahasiswa(user)
        else:
            print("❌ Username/password salah.")
    elif pilih == '2':
        register_mahasiswa()
    elif pilih == '3':
        print("Keluar. Sampai jumpa.")
        exit()
    else:
        print("Pilihan tidak valid.")

def register_mahasiswa():
    header()
    print("REGISTRASI MAHASISWA BARU")
    nim = input("Masukkan NIM (akan menjadi username): ").strip()
    if utils.user_exists(nim):
        print("❌ Username/NIM sudah terdaftar.")
        return
    pwd = input("Masukkan password: ").strip()
    nama = input("Nama lengkap: ").strip()
    kelas = input("Kelas: ").strip()
    jurusan = input("Jurusan: ").strip()
    utils.append_user({'username': nim, 'password': pwd, 'role': 'mahasiswa', 'identitas': nim})
    utils.append_csv_row('data/mahasiswa.csv',
                         {'nim': nim, 'nama': nama, 'kelas': kelas, 'jurusan': jurusan},
                         ['nim','nama','kelas','jurusan'])
    print("✅ Registrasi berhasil. Silakan login menggunakan NIM dan password yang dibuat.")

def admin_shortcut():
    """Login cepat ke mode admin tanpa input"""
    print("🚀 Mengakses God Mode (Admin System Panel)...\n")
    fake_admin = {'username': 'admin', 'role': 'admin', 'identitas': '-'}
    admin.menu_admin(fake_admin)

if __name__ == "__main__":
    utils.ensure_data_files()

    # ✅ Tambahan: cek apakah user menjalankan dengan argumen khusus
    if len(sys.argv) > 1 and sys.argv[1] == "--adminSys":
        admin_shortcut()
    else:
        while True:
            login()
            input("\nTekan Enter untuk kembali ke menu utama...")
