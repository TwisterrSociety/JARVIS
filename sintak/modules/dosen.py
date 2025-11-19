from modules import utils
import datetime
import uuid
import os

def header(user):
    print("=" * 60)
    print(f"🎓 Menu Dosen | Login sebagai: {user['username']}")
    print("=" * 60)

def menu_dosen(user):
    while True:
        header(user)
        print("[1] Lihat Daftar Mahasiswa")
        print("[2] Kelola Nilai")
        print("[3] Kelola Tugas")
        print("[4] Kelola Kehadiran")
        print("[5] Export Nilai")
        print("[6] Logout")

        pilih = input("Pilih: ").strip()

        if pilih == '1':
            lihat_mahasiswa()
        elif pilih == '2':
            kelola_nilai(user)
        elif pilih == '3':
            kelola_tugas(user)
        elif pilih == '4':
            kelola_kehadiran(user)
        elif pilih == '5':
            export_nilai(user)
        elif pilih == '6':
            print("👋 Logout berhasil.\n")
            break
        else:
            print("❌ Pilihan tidak valid.")

        input("\nTekan Enter untuk kembali ke menu...")

def lihat_mahasiswa():
    print("=" * 60)
    print("📚 DAFTAR MAHASISWA")
    print("=" * 60)

    data = utils.read_csv("data/mahasiswa.csv")
    if not data:
        print("Tidak ada data mahasiswa.")
        return

    print(f"{'NIM':<15} {'Nama':<30} {'Kelas':<10} {'Jurusan':<20}")
    print("-" * 75)

    for d in data:
        print(f"{d['nim']:<15} {d['nama']:<30} {d['kelas']:<10} {d['jurusan']:<20}")

def kelola_nilai(user):
    while True:
        print("\n=== KELOLA NILAI ===")
        print("[1] Lihat Nilai")
        print("[2] Tambah Nilai")
        print("[3] Edit Nilai")
        print("[4] Kembali")

        p = input("Pilih: ").strip()

        if p == '1':
            lihat_nilai(user)
        elif p == '2':
            tambah_nilai(user)
        elif p == '3':
            edit_nilai(user)
        elif p == '4':
            break
        else:
            print("❌ Pilihan tidak valid.")

def lihat_nilai(user):
    data = utils.read_csv('data/nilai.csv')

    print("\n📊 DATA NILAI")
    print("-" * 60)

    if not data:
        print("Belum ada data nilai.")
        return

    print(f"{'NIM':<15} {'Matkul':<20} {'Nilai':<8} {'Semester':<10}")

    for d in data:
        if d['mata_kuliah'] in user['mata_kuliah']:
            print(f"{d['nim']:<15} {d['mata_kuliah']:<20} {d['nilai']:<8} {d['semester']:<10}")

def tambah_nilai(user):
    print("\n➕ TAMBAH NILAI")
    nim = input("Masukkan NIM: ").strip()
    mk = input("Mata Kuliah: ").strip()

    if mk not in user['mata_kuliah']:
        print("❌ Anda tidak mengampu mata kuliah itu!")
        return

    n = input("Nilai: ").strip()
    s = input("SKS: ").strip()
    sm = input("Semester: ").strip()

    utils.append_csv_row(
        'data/nilai.csv',
        {
            'nim': nim,
            'mata_kuliah': mk,
            'nilai': n,
            'sks': s,
            'semester': sm
        },
        ['nim', 'mata_kuliah', 'nilai', 'sks', 'semester']
    )

    print("✅ Nilai ditambahkan.")

def edit_nilai(user):
    print("\n✏️ EDIT NILAI")
    nim = input("Masukkan NIM: ").strip()
    mk = input("Mata Kuliah: ").strip()

    data = utils.read_csv('data/nilai.csv')
    ketemu = False

    for d in data:
        if d['nim'] == nim and d['mata_kuliah'] == mk:

            if mk not in user['mata_kuliah']:
                print("❌ Anda tidak mengampu mata kuliah ini.")
                return

            print(f"Nilai saat ini: {d['nilai']}")
            nb = input("Nilai baru: ").strip()

            d['nilai'] = nb
            ketemu = True
            break

    if not ketemu:
        print("❌ Data nilai tidak ditemukan.")
        return

    utils.write_csv('data/nilai.csv', data, ['nim', 'mata_kuliah', 'nilai', 'sks', 'semester'])
    print("✅ Nilai diperbarui.")

def kelola_tugas(user):
    print("\n=== KELOLA TUGAS ===")
    print("[1] Lihat Tugas")
    print("[2] Buat Tugas")
    print("[3] Kembali")

    p = input("Pilih: ")

    if p == '1':
        lihat_tugas(user)
    elif p == '2':
        buat_tugas(user)
    elif p == '3':
        return
    else:
        print("❌ Pilihan tidak valid.")

def lihat_tugas(user):
    data = utils.read_csv("data/tugas.csv")

    if not data:
        print("Tidak ada tugas.")
        return

    print(f"{'ID':<10} {'Matkul':<20} {'Judul':<25} {'Deadline':<12}")
    print("-" * 75)

    for t in data:
        if t['mata_kuliah'] in user['mata_kuliah']:
            print(f"{t['id']:<10} {t['mata_kuliah']:<20} {t['judul']:<25} {t['deadline']:<12}")

def buat_tugas(user):
    print("\n📝 BUAT TUGAS")

    mk = input("Mata Kuliah: ").strip()
    if mk not in user['mata_kuliah']:
        print("❌ Anda tidak mengampu mata kuliah itu!")
        return

    j = input("Judul: ").strip()
    d = input("Deskripsi: ").strip()
    dl = input("Deadline (YYYY-MM-DD): ").strip()

    id_t = str(uuid.uuid4())[:8]

    utils.append_csv_row(
        'data/tugas.csv',
        {
            'id': id_t,
            'mata_kuliah': mk,
            'judul': j,
            'deskripsi': d,
            'deadline': dl
        },
        ['id', 'mata_kuliah', 'judul', 'deskripsi', 'deadline']
    )

    print("✅ Tugas dibuat.")

def kelola_kehadiran(user):
    print("\n=== KEHADIRAN ===")
    print("[1] Lihat Kehadiran")
    print("[2] Input Kehadiran")
    print("[3] Kembali")

    p = input("Pilih: ")

    if p == '1':
        lihat_kehadiran(user)
    elif p == '2':
        tambah_kehadiran(user)
    elif p == '3':
        return
    else:
        print("❌ Pilihan tidak valid.")

def lihat_kehadiran(user):
    data = utils.read_csv("data/kehadiran.csv")
    
    if not data:
        print("Belum ada data.")
        return

    print(f"{'NIM':<15} {'Matkul':<20} {'Tanggal':<12} {'Status':<10}")
    print("-" * 60)

    for h in data:
        if h['mata_kuliah'] in user['mata_kuliah']:
            print(f"{h['nim']:<15} {h['mata_kuliah']:<20} {h['tanggal']:<12} {h['status']:<10}")

def tambah_kehadiran(user):
    print("\n➕ INPUT KEHADIRAN")

    nim = input("NIM: ").strip()
    mk = input("Mata Kuliah: ").strip()

    if mk not in user['mata_kuliah']:
        print("❌ Anda tidak mengampu MK itu!")
        return

    tgl = input("Tanggal (kosong = hari ini): ").strip()
    if tgl == "":
        tgl = datetime.date.today().isoformat()

    st = input("Status (Hadir/Izin/Alfa): ").strip()

    utils.append_csv_row(
        'data/kehadiran.csv',
        {'nim': nim, 'mata_kuliah': mk, 'tanggal': tgl, 'status': st},
        ['nim', 'mata_kuliah', 'tanggal', 'status']
    )

    print("✅ Kehadiran ditambah.")

def export_nilai(user):
    data = utils.read_csv("data/nilai.csv")
    flt = [d for d in data if d['mata_kuliah'] in user['mata_kuliah']]

    if not flt:
        print("❌ Tidak ada nilai untuk MK Anda.")
        return

    os.makedirs("exports", exist_ok=True)
    path = f"exports/nilai_{user['id']}.txt"

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"LAPORAN NILAI: {user['username']}\n")
        f.write("=" * 50 + "\n\n")

        for d in flt:
            f.write(
                f"NIM: {d['nim']} | MK: {d['mata_kuliah']} | "
                f"Nilai: {d['nilai']} | Semester: {d['semester']} | SKS: {d['sks']}\n"
            )

    print(f"✅ File disimpan: {path}")
