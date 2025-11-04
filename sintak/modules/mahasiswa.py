# modules/mahasiswa.py
from modules.utils import baca_csv, export_txt
from datetime import date

def menu_mahasiswa(user):
    # for mahasiswa, user['identitas'] is nim (or username may be nim)
    nim = user.get('identitas') or user.get('username')
    while True:
        print("="*45)
        print(f"🎓 MAHASISWA PANEL | {user.get('username')} (NIM: {nim})")
        print("="*45)
        print("1. Lihat Nilai & IPK")
        print("2. Lihat Tugas")
        print("3. Lihat Absensi")
        print("4. Export Data Saya (txt)")
        print("5. Kembali")
        pilih = input("Pilih: ").strip()
        if pilih == '1': lihat_nilai_ipk(nim)
        elif pilih == '2': lihat_tugas(nim)
        elif pilih == '3': lihat_absensi(nim)
        elif pilih == '4': export_data_me(nim, user.get('username'))
        elif pilih == '5': break
        else: print("Pilihan tidak valid.")

def lihat_nilai_ipk(nim):
    data = baca_csv('data/nilai.csv')
    my = [d for d in data if d['nim'] == nim]
    if not my:
        print("Belum ada nilai.")
        return
    total_sks = 0
    total_bobot = 0.0
    print("Daftar nilai:")
    for r in my:
        print(f"- {r['mata_kuliah']} : {r['nilai']} (SKS {r.get('sks','')})")
        try:
            sks = float(r.get('sks',0))
            nilai = float(r.get('nilai',0))
            total_sks += sks
            total_bobot += nilai * sks
        except:
            pass
    ipk = (total_bobot / total_sks) if total_sks>0 else 0
    print(f"\nIPK: {round(ipk,2)}")

def lihat_tugas(nim):
    data = baca_csv('data/tugas.csv')
    found = False
    for t in data:
        # tugas bersifat umum, mahasiswa lihat semua
        print(f"- [{t['status']}] {t['tugas']} ({t['mata_kuliah']}) Deadline: {t.get('deadline','')}")
        found = True
    if not found:
        print("Belum ada tugas terdaftar.")

def lihat_absensi(nim):
    data = baca_csv('data/absensi.csv')
    hadir = sum(1 for d in data if d['nim']==nim and d['status'].lower()=='hadir')
    izin = sum(1 for d in data if d['nim']==nim and d['status'].lower()=='izin')
    alfa = sum(1 for d in data if d['nim']==nim and d['status'].lower()=='alfa')
    print(f"Kehadiran: Hadir={hadir}, Izin={izin}, Alfa={alfa}")

def export_data_me(nim, username):
    nilai = baca_csv('data/nilai.csv')
    tugas = baca_csv('data/tugas.csv')
    absn = baca_csv('data/absensi.csv')
    s = f"=== LAPORAN MAHASISWA {nim} ===\nTanggal export: {date.today().isoformat()}\n\n"
    s += "NILAI:\n"
    for r in nilai:
        if r['nim']==nim:
            s += f"{r['mata_kuliah']} = {r['nilai']}\n"
    s += "\nTUGAS:\n"
    for r in tugas:
        s += f"{r['tugas']} ({r['mata_kuliah']}) - Status: {r['status']}\n"
    s += "\nABSENSI:\n"
    for r in absn:
        if r['nim']==nim:
            s += f"{r['tanggal']} | {r['mata_kuliah']} | {r['status']}\n"
    export_path = f"exports/laporan_{username}.txt"
    export_txt(export_path, s)
