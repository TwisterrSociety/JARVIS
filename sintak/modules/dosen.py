import csv
import sys

from modules import utils

def header():
    print("=" * 60)
    print("  🧩 SINTAK - Sistem Informasi Nilai, Tugas, dan Kehadiran (CLI)")
    print("=" * 60)

def menu_dosen(user):
    while True:
        header()
        print(f"Menu Dosen: {user['username']}")
        print("[1] Lihat Daftar Mahasiswa")
        print("[2] Kelola Nilai")
        print("[3] Kelola Tugas")
        print("[4] Kelola Kehadiran")
        print("[5] Logout")
        pilih = input("Pilih: ").strip()
        
        if pilih == '1':
            lihat_mahasiswa()
        elif pilih == '2':
            kelola_nilai()
        elif pilih == '3':
            kelola_tugas()
        elif pilih == '4':
            kelola_kehadiran()
        elif pilih == '5':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")
        
        input("\nTekan Enter untuk kembali ke menu...")

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

def kelola_nilai():
    header()
    print("KELOLA NILAI")
    print("[1] Lihat Nilai Mahasiswa")
    print("[2] Input/Edit Nilai")
    pilih = input("Pilih: ").strip()
    
    if pilih == '1':
        lihat_nilai()
    elif pilih == '2':
        input_nilai()
    else:
        print("Pilihan tidak valid.")

def lihat_nilai():
    header()
    print("LIHAT NILAI MAHASISWA")
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

def input_nilai():
    header()
    print("INPUT/EDIT NILAI")
    nim = input("NIM Mahasiswa: ").strip()
    mata_kuliah = input("Mata Kuliah: ").strip()
    nilai = input("Nilai: ").strip()
    
    if not utils.user_exists(nim):
        print("❌ Mahasiswa tidak ditemukan.")
        return
    nilai_list = utils.read_csv('data/nilai.csv') or []
    nilai_list = [n for n in nilai_list if not (n['nim'] == nim and n['mata_kuliah'] == mata_kuliah)]
    nilai_list.append({'nim': nim, 'mata_kuliah': mata_kuliah, 'nilai': nilai})
    utils.write_csv('data/nilai.csv', nilai_list, ['nim', 'mata_kuliah', 'nilai'])
    print("✅ Nilai berhasil disimpan.")

def kelola_tugas():
    header()
    print("KELOLA TUGAS")
    print("[1] Lihat Tugas Mahasiswa")
    print("[2] Input/Edit Tugas")
    pilih = input("Pilih: ").strip()
    
    if pilih == '1':
        lihat_tugas()
    elif pilih == '2':
        input_tugas()
    else:
        print("Pilihan tidak valid.")

def lihat_tugas():
    header()
    print("LIHAT TUGAS MAHASISWA")
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

def input_tugas():
    header()
    print("INPUT/EDIT TUGAS")
    nim = input("NIM Mahasiswa: ").strip()
    mata_kuliah = input("Mata Kuliah: ").strip()
    tugas = input("Nama Tugas: ").strip()
    status = input("Status (Selesai/Belum): ").strip()
    
    if not utils.user_exists(nim):
        print("❌ Mahasiswa tidak ditemukan.")
        return    
    tugas_list = utils.read_csv('data/tugas.csv') or []
    tugas_list = [t for t in tugas_list if not (t['nim'] == nim and t['mata_kuliah'] == mata_kuliah and t['tugas'] == tugas)]
    tugas_list.append({'nim': nim, 'mata_kuliah': mata_kuliah, 'tugas': tugas, 'status': status})
    
    utils.write_csv('data/tugas.csv', tugas_list, ['nim', 'mata_kuliah', 'tugas', 'status'])
    print("✅ Tugas berhasil disimpan.")

def kelola_kehadiran():
    header()
    print("KELOLA KEHADIRAN")
    print("[1] Lihat Kehadiran Mahasiswa")
    print("[2] Input/Edit Kehadiran")
    pilih = input("Pilih: ").strip()
    
    if pilih == '1':
        lihat_kehadiran()
    elif pilih == '2':
        input_kehadiran()
    else:
        print("Pilihan tidak valid.")

def lihat_kehadiran():
    header()
    print("LIHAT KEHADIRAN MAHASISWA")
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

def input_kehadiran():
    header()
    print("INPUT/EDIT KEHADIRAN")
    nim = input("NIM Mahasiswa: ").strip()
    mata_kuliah = input("Mata Kuliah: ").strip()
    tanggal = input("Tanggal (YYYY-MM-DD): ").strip()
    status = input("Status (Hadir/Tidak): ").strip()
    
    if not utils.user_exists(nim):
        print("❌ Mahasiswa tidak ditemukan.")
        return
    kehadiran_list = utils.read_csv('data/kehadiran.csv') or []
    kehadiran_list = [k for k in kehadiran_list if not (k['nim'] == nim and k['mata_kuliah'] == mata_kuliah and k['tanggal'] == tanggal)]
    kehadiran_list.append({'nim': nim, 'mata_kuliah': mata_kuliah, 'tanggal': tanggal, 'status': status})
    
    utils.write_csv('data/kehadiran.csv', kehadiran_list, ['nim', 'mata_kuliah', 'tanggal', 'status'])
    print("✅ Kehadiran berhasil disimpan.")
