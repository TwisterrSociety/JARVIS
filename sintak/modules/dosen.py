# modules/dosen.py
from modules.utils import baca_csv, append_csv_row, tulis_csv, get_dosen_by_user
import uuid

def menu_dosen(user):
    # user['identitas'] harus berisi id_dosen
    id_dosen = user.get('identitas','')
    while True:
        print("="*45)
        print(f"👨‍🏫 DOSEN PANEL | {user['username']} (ID: {id_dosen})")
        print("="*45)
        print("1. Input Nilai Mahasiswa")
        print("2. Input Absensi")
        print("3. Buat Tugas")
        print("4. Lihat Nilai Kelas")
        print("5. Export Nilai (txt)")
        print("6. Kembali")
        pilih = input("Pilih: ").strip()
        if pilih == '1': input_nilai(id_dosen)
        elif pilih == '2': input_absensi(id_dosen)
        elif pilih == '3': buat_tugas(id_dosen)
        elif pilih == '4': lihat_nilai_kelas(id_dosen)
        elif pilih == '5': export_nilai_dosen(id_dosen)
        elif pilih == '6': break
        else: print("Pilihan tidak valid.")

def allowed_matkul_for_dosen(id_dosen):
    dos = baca_csv('data/dosen.csv')
    for d in dos:
        if d['id_dosen'] == id_dosen:
            # mata_kuliah bisa dipisah koma
            return [m.strip() for m in d['mata_kuliah'].split(',')]
    return []

def input_nilai(id_dosen):
    allowed = allowed_matkul_for_dosen(id_dosen)
    if not allowed:
        print("Anda belum memiliki mata kuliah terdaftar.")
        return
    print("Mata kuliah Anda:", allowed)
    mk = input("Mata Kuliah (pilih dari list di atas): ").strip()
    if mk not in allowed:
        print("Tidak diijinkan memasukkan nilai untuk mata kuliah ini.")
        return
    nim = input("NIM Mahasiswa: ").strip()
    nilai = input("Nilai: ").strip()
    sks = input("SKS: ").strip()
    append_csv_row('data/nilai.csv', {'nim':nim,'mata_kuliah':mk,'nilai':nilai,'sks':sks},
                   ['nim','mata_kuliah','nilai','sks'])
    print("Nilai ditambahkan.")

def input_absensi(id_dosen):
    allowed = allowed_matkul_for_dosen(id_dosen)
    print("Mata kuliah Anda:", allowed)
    mk = input("Mata Kuliah: ").strip()
    if mk not in allowed:
        print("Tidak diizinkan.")
        return
    nim = input("NIM: ").strip()
    tanggal = input("Tanggal (YYYY-MM-DD) [Enter untuk hari ini]: ").strip()
    if not tanggal:
        from datetime import date
        tanggal = date.today().isoformat()
    status = input("Status (Hadir/Izin/Alfa): ").strip()
    ket = input("Keterangan (opsional): ").strip()
    append_csv_row('data/absensi.csv', {'nim':nim,'mata_kuliah':mk,'tanggal':tanggal,'status':status,'keterangan':ket},
                   ['nim','mata_kuliah','tanggal','status','keterangan'])
    print("Absensi dicatat.")

def buat_tugas(id_dosen):
    allowed = allowed_matkul_for_dosen(id_dosen)
    print("Mata kuliah Anda:", allowed)
    mk = input("Mata Kuliah: ").strip()
    if mk not in allowed:
        print("Tidak diijinkan membuat tugas untuk mata kuliah ini.")
        return
    idt = str(uuid.uuid4())[:8]
    tugas = input("Nama tugas: ").strip()
    des = input("Deskripsi: ").strip()
    dl = input("Deadline (YYYY-MM-DD): ").strip()
    append_csv_row('data/tugas.csv',
                   {'id_tugas':idt,'mata_kuliah':mk,'dosen_id':id_dosen,'tugas':tugas,'deskripsi':des,'deadline':dl,'status':'Belum'},
                   ['id_tugas','mata_kuliah','dosen_id','tugas','deskripsi','deadline','status'])
    print("Tugas dibuat.")

def lihat_nilai_kelas(id_dosen):
    allowed = allowed_matkul_for_dosen(id_dosen)
    nilai = baca_csv('data/nilai.csv')
    for n in nilai:
        if n['mata_kuliah'] in allowed:
            print(f"{n['nim']} | {n['mata_kuliah']} = {n['nilai']}")

def export_nilai_dosen(id_dosen):
    allowed = allowed_matkul_for_dosen(id_dosen)
    nilai = baca_csv('data/nilai.csv')
    s = f"=== LAPORAN NILAI DOSEN {id_dosen} ===\n"
    for n in nilai:
        if n['mata_kuliah'] in allowed:
            s += f"{n['nim']} | {n['mata_kuliah']} = {n['nilai']}\n"
    export_path = f"exports/laporan_nilai_{id_dosen}.txt"
    from modules.utils import export_txt
    export_txt(export_path, s)
