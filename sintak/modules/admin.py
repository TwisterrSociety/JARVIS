import csv
from modules import utils

def header():
    print("=" * 60)
    print("  🧩 SINTAK - Sistem Informasi Nilai, Tugas, dan Kehadiran (CLI)")
    print("=" * 60)

def menu_admin(user):
    while True:
        header()
        print(f"Menu Admin: {user['username']}")
        print("[1] Lihat Daftar User")
        print("[2] Tambah User")
        print("[3] Hapus User")
        print("[4] Lihat Data Mahasiswa")
        print("[5] Lihat Data Nilai")
        print("[6] Lihat Data Tugas")
        print("[7] Lihat Data Kehadiran")
        print("[8] Logout")
        pilih = input("Pilih: ").strip()
        
        if pilih == '1':
            lihat_user()
        elif pilih == '2':
            tambah_user()
        elif pilih == '3':
            hapus_user()
        elif pilih == '4':
            lihat_mahasiswa()
        elif pilih == '5':
            lihat_nilai()
        elif pilih == '6':
            lihat_tugas()
        elif pilih == '7':
            lihat_kehadiran()
        elif pilih == '8':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")
        
        input("\nTekan Enter untuk kembali ke menu...")

def lihat_user():
    header()
    print("DAFTAR USER")
    try:
        users = utils.read_csv('data/users.csv')
        if users:
            print(f"{'Username':<20} {'Role':<15} {'Identitas':<20}")
            print("-" * 55)
            for u in users:
                print(f"{u['username']:<20} {u['role']:<15} {u['identitas']:<20}")
        else:
            print("Tidak ada data user.")
    except FileNotFoundError:
        print("File data/users.csv tidak ditemukan.")

def tambah_user():
    header()
    print("TAMBAH USER BARU")
    username = input("Username: ").strip()
    if utils.user_exists(username):
        print("❌ Username sudah ada.")
        return
    password = input("Password: ").strip()
    role = input("Role (admin/dosen/mahasiswa): ").strip().lower()
    if role not in ['admin', 'dosen', 'mahasiswa']:
        print("❌ Role tidak valid.")
        return
    identitas = input("Identitas (NIM untuk mahasiswa, atau - untuk lainnya): ").strip()
    
    utils.append_user({'username': username, 'password': password, 'role': role, 'identitas': identitas})
    
    if role == 'mahasiswa':
        nama = input("Nama lengkap: ").strip()
        kelas = input("Kelas: ").strip()
        jurusan = input("Jurusan: ").strip()
        utils.append_csv_row('data/mahasiswa.csv',
                             {'nim': identitas, 'nama': nama, 'kelas': kelas, 'jurusan': jurusan},
                             ['nim','nama','kelas','jurusan'])
    
    print("✅ User berhasil ditambahkan.")

def hapus_user():
    header()
    print("HAPUS USER")
    username = input("Username yang akan dihapus: ").strip()
    if not utils.user_exists(username):
        print("❌ User tidak ditemukan.")
        return
    
    # Hapus dari users.csv
    users = utils.read_csv('data/users.csv')
    users = [u for u in users if u['username'] != username]
    utils.write_csv('data/users.csv', users, ['username', 'password', 'role', 'identitas'])
    
    # Jika mahasiswa, hapus juga dari mahasiswa.csv
    user = utils.find_user(username, '')  # Cari tanpa password
    if user and user['role'] == 'mahasiswa':
        mahasiswa_list = utils.read_csv('data/mahasiswa.csv')
        mahasiswa_list = [m for m in mahasiswa_list if m['nim'] != user['identitas']]
        utils.write_csv('data/mahasiswa.csv', mahasiswa_list, ['nim', 'nama', 'kelas', 'jurusan'])
    
    print("✅ User berhasil dihapus.")

def lihat_mahasiswa():
    header()
    print("DAFTAR MAHASISWA")
    try:
        mahasiswa_list = utils.read_csv('data/mahasiswa.csv')
        if mahasiswa_list:
            print(f"{'NIM':<15} {'Nama':<30} {'Kelas':<10} {'Jurusan':<20}")
            print("-" * 75)
            for mhs in mahasiswa_list:
                print(f"{mhs['nim']:<15} {mhs['nama']:<30} {mhs['kelas']:<10} {mhs['jurusan']:<20}")
        else:
            print("Tidak ada data mahasiswa.")
    except FileNotFoundError:
        print("File data/mahasiswa.csv tidak ditemukan.")

def lihat_nilai():
    header()
    print("DAFTAR NILAI")
    try:
        nilai_list = utils.read_csv('data/nilai.csv')
        if nilai_list:
            print(f"{'NIM':<15} {'Mata Kuliah':<20} {'Nilai':<10}")
            print("-" * 45)
            for n in nilai_list:
                print(f"{n['nim']:<15} {n['mata_kuliah']:<20} {n['nilai']:<10}")
        else:
            print("Tidak ada data nilai.")
    except FileNotFoundError:
        print("File data/nilai.csv tidak ditemukan.")

def lihat_tugas():
    header()
    print("DAFTAR TUGAS")
    try:
        tugas_list = utils.read_csv('data/tugas.csv')
        if tugas_list:
            print(f"{'NIM':<15} {'Mata Kuliah':<20} {'Tugas':<30} {'Status':<10}")
            print("-" * 75)
            for t in tugas_list:
                print(f"{t['nim']:<15} {t['mata_kuliah']:<20} {t['tugas']:<30} {t['status']:<10}")
        else:
            print("Tidak ada data tugas.")
    except FileNotFoundError:
        print("File data/tugas.csv tidak ditemukan.")

def lihat_kehadiran():
    header()
    print("DAFTAR KEHADIRAN")
    try:
        kehadiran_list = utils.read_csv('data/kehadiran.csv')
        if kehadiran_list:
            print(f"{'NIM':<15} {'Mata Kuliah':<20} {'Tanggal':<12} {'Status':<10}")
            print("-" * 57)
            for k in kehadiran_list:
                print(f"{k['nim']:<15} {k['mata_kuliah']:<20} {k['tanggal']:<12} {k['status']:<10}")
        else:
            print("Tidak ada data kehadiran.")
    except FileNotFoundError:
        print("File data/kehadiran.csv tidak ditemukan.")