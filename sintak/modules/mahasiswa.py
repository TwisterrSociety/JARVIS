from modules import utils

def menu_mahasiswa(user):
    while True:
        print("=" * 60)
        print(f"🎓 Menu Mahasiswa | Login sebagai: {user['username']}")
        print("=" * 60)
        print("[1] Lihat Profil")
        print("[2] Lihat Nilai")
        print("[3] Lihat Kehadiran")
        print("[4] Logout")

        pilih = input("Pilih menu: ").strip()
        if pilih == '1':
            lihat_profil(user)
        elif pilih == '2':
            lihat_nilai(user)
        elif pilih == '3':
            lihat_kehadiran(user)
        elif pilih == '4':
            print("👋 Logout berhasil. Kembali ke menu utama.\n")
            break
        else:
            print("❌ Pilihan tidak valid.\n")

def lihat_profil(user):
    """Tampilkan profil mahasiswa berdasarkan NIM."""
    nim = user['identitas']
    data = utils.read_csv('data/mahasiswa.csv')
    mahasiswa = next((m for m in data if m['nim'] == nim), None)

    if not mahasiswa:
        print("❌ Data mahasiswa tidak ditemukan.")
        return

    print("\n🪪 PROFIL MAHASISWA")
    print("-" * 60)
    print(f"NIM      : {mahasiswa['nim']}")
    print(f"Nama     : {mahasiswa['nama']}")
    print(f"Kelas    : {mahasiswa['kelas']}")
    print(f"Jurusan  : {mahasiswa['jurusan']}")
    print("-" * 60)

def lihat_nilai(user):
    """Menampilkan nilai mahasiswa yang sedang login."""
    nim = user['identitas']
    data_nilai = utils.read_csv('data/nilai.csv')
    nilai = next((n for n in data_nilai if n['nim'] == nim), None)

    print("\n📊 NILAI MAHASISWA")
    print("-" * 40)
    if nilai:
        print(f"NIM   : {nilai['nim']}")
        print(f"Nama  : {nilai['nama']}")
        print(f"Nilai : {nilai['nilai']}")
    else:
        print("Belum ada data nilai.")
    print("-" * 40)

def lihat_kehadiran(user):
    """Menampilkan data kehadiran mahasiswa yang sedang login."""
    nim = user['identitas']
    data_hadir = utils.read_csv('data/kehadiran.csv')
    hadir_list = [h for h in data_hadir if h['nim'] == nim]

    print("\n📅 KEHADIRAN MAHASISWA")
    print("-" * 60)
    print(f"{'Tanggal':<15} {'Status':<10}")
    print("-" * 60)

    if not hadir_list:
        print("Belum ada data kehadiran.")
    else:
        for h in hadir_list:
            print(f"{h['tanggal']:<15} {h['status']:<10}")
    print("-" * 60)
