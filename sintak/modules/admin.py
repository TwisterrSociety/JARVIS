# modules/admin.py
from modules.utils import baca_csv, tulis_csv, append_csv_row, export_txt
import uuid

def menu_admin(user):
    while True:
        print("="*50)
        print("👑 ADMIN PANEL - GOD MODE")
        print("="*50)
        print("1. Manajemen User (Admin/Dosen/Mahasiswa)")
        print("2. Kelola Data Mahasiswa")
        print("3. Kelola Data Dosen")
        print("4. Kelola Nilai")
        print("5. Kelola Tugas")
        print("6. Kelola Absensi")
        print("7. Export semua data ke .txt")
        print("8. Logout")
        pilih = input("Pilih: ").strip()
        if pilih == '1': manage_users()
        elif pilih == '2': manage_mahasiswa()
        elif pilih == '3': manage_dosen()
        elif pilih == '4': manage_nilai()
        elif pilih == '5': manage_tugas()
        elif pilih == '6': manage_absensi()
        elif pilih == '7': export_all()
        elif pilih == '8': break
        else: print("Pilihan tidak valid.")

# ---- USER (god) ----
def manage_users():
    users = baca_csv('data/users.csv')
    print("[1] Tampilkan user  [2] Tambah user  [3] Hapus user")
    c = input("Pilih: ").strip()
    if c == '1':
        for u in users:
            print(f"{u['username']} | role: {u['role']} | identitas: {u.get('identitas','')}")
    elif c == '2':
        username = input("username: ").strip()
        if any(x['username']==username for x in users):
            print("Sudah ada.")
            return
        pwd = input("password: ").strip()
        role = input("role (admin/dosen/mahasiswa): ").strip()
        ident = input("identitas (nim atau id_dosen, atau -): ").strip() or '-'
        append_csv_row('data/users.csv', {'username':username,'password':pwd,'role':role,'identitas':ident},
                       ['username','password','role','identitas'])
        print("User ditambahkan.")
    elif c == '3':
        target = input("Masukkan username yang dihapus: ").strip()
        users = [u for u in users if u['username'] != target]
        tulis_csv('data/users.csv', users, ['username','password','role','identitas'])
        print("User dihapus.")

# ---- MAHASISWA ----
def manage_mahasiswa():
    rows = baca_csv('data/mahasiswa.csv')
    print("[1] Tampilkan  [2] Tambah  [3] Hapus")
    c = input("Pilih: ").strip()
    if c == '1':
        for r in rows: print(f"{r['nim']} | {r['nama']} | {r['kelas']} | {r['jurusan']}")
    elif c == '2':
        nim = input("NIM: "); nama = input("Nama: "); kelas = input("Kelas: "); jur = input("Jurusan: ")
        append_csv_row('data/mahasiswa.csv', {'nim':nim,'nama':nama,'kelas':kelas,'jurusan':jur},
                       ['nim','nama','kelas','jurusan'])
        print("Mahasiswa ditambahkan.")
    elif c == '3':
        nim = input("NIM hapus: ")
        rows = [r for r in rows if r['nim'] != nim]
        tulis_csv('data/mahasiswa.csv', rows, ['nim','nama','kelas','jurusan'])
        print("Dihapus.")

# ---- DOSEN ----
def manage_dosen():
    rows = baca_csv('data/dosen.csv')
    print("[1] Tampilkan  [2] Tambah  [3] Hapus")
    c = input("Pilih: ").strip()
    if c == '1':
        for r in rows: print(f"{r['id_dosen']} | {r['nama_dosen']} | {r['mata_kuliah']}")
    elif c == '2':
        idd = input("ID Dosen (unik): "); nama = input("Nama Dosen: "); mk = input("Mata Kuliah (pisah koma jika lebih): ")
        append_csv_row('data/dosen.csv', {'id_dosen':idd,'nama_dosen':nama,'mata_kuliah':mk},
                       ['id_dosen','nama_dosen','mata_kuliah'])
        print("Dosen ditambahkan.")
    elif c == '3':
        idd = input("ID Dosen hapus: ")
        rows = [r for r in rows if r['id_dosen'] != idd]
        tulis_csv('data/dosen.csv', rows, ['id_dosen','nama_dosen','mata_kuliah'])
        print("Dosen dihapus.")

# ---- NILAI ----
def manage_nilai():
    rows = baca_csv('data/nilai.csv')
    print("[1] Tampilkan  [2] Tambah  [3] Hapus")
    c = input("Pilih: ").strip()
    if c == '1':
        for r in rows: print(f"{r['nim']} | {r['mata_kuliah']} = {r['nilai']} (SKS:{r.get('sks','')})")
    elif c == '2':
        nim = input("NIM: "); mk = input("Mata Kuliah: "); nilai = input("Nilai: "); sks = input("SKS: ")
        append_csv_row('data/nilai.csv', {'nim':nim,'mata_kuliah':mk,'nilai':nilai,'sks':sks},
                       ['nim','mata_kuliah','nilai','sks'])
        print("Nilai ditambahkan.")
    elif c == '3':
        nim = input("Hapus semua nilai NIM: ")
        rows = [r for r in rows if r['nim'] != nim]
        tulis_csv('data/nilai.csv', rows, ['nim','mata_kuliah','nilai','sks'])
        print("Dihapus.")

# ---- TUGAS ----
def manage_tugas():
    rows = baca_csv('data/tugas.csv')
    print("[1] Tampilkan  [2] Tambah  [3] Ubah status  [4] Hapus")
    c = input("Pilih: ").strip()
    if c == '1':
        for r in rows: print(f"{r['id_tugas']} | {r['mata_kuliah']} | {r['tugas']} | {r['status']}")
    elif c == '2':
        idt = str(uuid.uuid4())[:8]
        mk = input("Mata Kuliah: "); dos = input("Dosen ID: ")
        tugas = input("Nama tugas: "); des = input("Deskripsi: "); dl = input("Deadline: ")
        append_csv_row('data/tugas.csv',
                       {'id_tugas':idt,'mata_kuliah':mk,'dosen_id':dos,'tugas':tugas,'deskripsi':des,'deadline':dl,'status':'Belum'},
                       ['id_tugas','mata_kuliah','dosen_id','tugas','deskripsi','deadline','status'])
        print("Tugas ditambahkan.")
    elif c == '3':
        idt = input("ID tugas untuk ubah status: ")
        for r in rows:
            if r['id_tugas']==idt:
                r['status'] = input("Masukkan status baru (Belum/Selesai): ")
        tulis_csv('data/tugas.csv', rows, ['id_tugas','mata_kuliah','dosen_id','tugas','deskripsi','deadline','status'])
        print("Status diubah.")
    elif c == '4':
        idt = input("ID tugas hapus: ")
        rows = [r for r in rows if r['id_tugas'] != idt]
        tulis_csv('data/tugas.csv', rows, ['id_tugas','mata_kuliah','dosen_id','tugas','deskripsi','deadline','status'])
        print("Dihapus.")

# ---- ABSENSI ----
def manage_absensi():
    rows = baca_csv('data/absensi.csv')
    print("[1] Tampilkan  [2] Tambah  [3] Hapus")
    c = input("Pilih: ").strip()
    if c == '1':
        for r in rows: print(f"{r['nim']} | {r['mata_kuliah']} | {r['tanggal']} | {r['status']} | {r.get('keterangan','')}")
    elif c == '2':
        nim = input("NIM: "); mk = input("Mata Kuliah: "); tgl = input("Tanggal (YYYY-MM-DD): ")
        st = input("Status (Hadir/Izin/Alfa): "); ket = input("Keterangan (opsional): ")
        append_csv_row('data/absensi.csv', {'nim':nim,'mata_kuliah':mk,'tanggal':tgl,'status':st,'keterangan':ket},
                       ['nim','mata_kuliah','tanggal','status','keterangan'])
        print("Absensi ditambahkan.")
    elif c == '3':
        nim = input("Hapus absensi NIM: ")
        rows = [r for r in rows if r['nim'] != nim]
        tulis_csv('data/absensi.csv', rows, ['nim','mata_kuliah','tanggal','status','keterangan'])
        print("Dihapus.")

# ---- EXPORT ALL ----
def export_all():
    mhs = baca_csv('data/mahasiswa.csv')
    nilai = baca_csv('data/nilai.csv')
    tugas = baca_csv('data/tugas.csv')
    absn = baca_csv('data/absensi.csv')

    s = "=== LAPORAN SINTAK (ADMIN) ===\n\nMAHASISWA:\n"
    for r in mhs:
        s += f"{r['nim']} | {r['nama']} | {r['kelas']} | {r['jurusan']}\n"
    s += "\nNILAI:\n"
    for r in nilai:
        s += f"{r['nim']} | {r['mata_kuliah']} = {r['nilai']} (SKS {r.get('sks','')})\n"
    s += "\nTUGAS:\n"
    for r in tugas:
        s += f"{r['id_tugas']} | {r['mata_kuliah']} | {r['tugas']} | {r['status']}\n"
    s += "\nABSENSI:\n"
    for r in absn:
        s += f"{r['nim']} | {r['mata_kuliah']} | {r['tanggal']} | {r['status']}\n"

    export_txt('exports/laporan_admin.txt', s)
