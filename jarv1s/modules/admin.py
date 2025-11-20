# modules/admin.py
import json
from modules.utils import (
    typing, pause, read_txt, write_txt, append_txt,
    append_txt_row, append_user, export_txt, gen_id, today,
    rand_password, push_notification, get_notifications_for,
    search, multisearch, sort_data
)

# small wrappers
def _read(p): return read_txt(p)
def _write(p, d): return write_txt(p, d)
def _append(p, d): return append_txt(p, d)

# ----------------------------
# Admin main menu
# ----------------------------
def menu_admin(user):
    while True:
        print("\n" + "="*60)
        print("👑 ADMIN PANEL - SINTAK")
        print("="*60)
        print("1. Manajemen User")
        print("2. Kelola Mahasiswa")
        print("3. Kelola Dosen")
        print("4. Kelola Mata Kuliah")
        print("5. Kelola Nilai / Transkrip")
        print("6. Kelola Tugas / Absensi")
        print("7. SPP / Pembayaran")
        print("8. Bus Tracking")
        print("9. E-Library")
        print("10. Notifikasi / Pengumuman")
        print("11. Manajemen Grup Chat")
        print("12. Export Semua Data")
        print("13. Logout")
        print("="*60)
        pilih = input("Pilih: ").strip()
        if pilih == '1': manage_users()
        elif pilih == '2': manage_mahasiswa()
        elif pilih == '3': manage_dosen()
        elif pilih == '4': manage_matkul()
        elif pilih == '5': manage_nilai()
        elif pilih == '6': manage_tugas_absensi()
        elif pilih == '7': manage_spp()
        elif pilih == '8': manage_bus()
        elif pilih == '9': manage_elibrary()
        elif pilih == '10': manage_notifications()
        elif pilih == '11': manage_chat_groups()
        elif pilih == '12': export_all_data()
        elif pilih == '13':
            typing("🔒 Logout...", 0.01)
            break
        else:
            typing("Pilihan tidak valid.", 0.01)

# ----------------------------
# 1. Manage users
# ----------------------------
def manage_users():
    while True:
        print("\n--- Manajemen User ---")
        print("1. Lihat semua user")
        print("2. Hapus user")
        print("3. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            users = _read("data/users.txt")
            if not users:
                typing(" (kosong) ", 0.01)
            for u in users:
                print(f"- {u.get('username')} | role: {u.get('role')} | identitas: {u.get('identitas')}")
            pause()
        elif c == '2':
            t = input("Username yang dihapus: ").strip()
            users = _read("data/users.txt")
            users = [u for u in users if u.get("username") != t]
            _write("data/users.txt", users)
            typing("✔ User dihapus.", 0.01)
        else:
            break

# ----------------------------
# 2. Kelola Mahasiswa
# ----------------------------
def manage_mahasiswa():
    while True:
        print("\n--- Kelola Mahasiswa ---")
        print("1. Lihat Mahasiswa")
        print("2. Tambah Mahasiswa")
        print("3. Hapus Mahasiswa")
        print("4. Edit Mahasiswa")
        print("5. Search & Sort Mahasiswa")
        print("6. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            data = _read("data/mahasiswa.txt")
            for m in data:
                print(f"{m.get('nim')} | {m.get('nama')} | {m.get('kelas','-')} | {m.get('jurusan','-')}")
            pause()
        elif c == '2':
            nim = input("NIM: ").strip()
            nama = input("Nama: ").strip()
            kelas = input("Kelas (opsional): ").strip()
            jur = input("Jurusan (opsional): ").strip()
            _append("data/mahasiswa.txt", {"nim":nim,"nama":nama,"kelas":kelas,"jurusan":jur})
            # create login user for mahasiswa (auto password)
            pwd = rand_password()
            append_user({"username":nim,"password":pwd,"role":"mahasiswa","identitas":nim})
            typing(f"✔ Mahasiswa dan akun dibuat. Password: {pwd}", 0.02)
        elif c == '3':
            nim = input("NIM hapus: ").strip()
            data = _read("data/mahasiswa.txt")
            data = [d for d in data if d.get("nim") != nim]
            _write("data/mahasiswa.txt", data)
            users = _read("data/users.txt")
            users = [u for u in users if not (u.get("role")=="mahasiswa" and u.get("identitas")==nim)]
            _write("data/users.txt", users)
            typing("✔ Mahasiswa dihapus.", 0.01)
        elif c == '4':
            nim = input("NIM edit: ").strip()
            data = _read("data/mahasiswa.txt")
            for d in data:
                if d.get("nim")==nim:
                    print("Field yang bisa diedit: nama, kelas, jurusan, hp, email, ttl, jk")
                    field = input("Field: ").strip()
                    if field in d:
                        d[field] = input("Nilai baru: ").strip()
            _write("data/mahasiswa.txt", data)
            typing("✔ Data diupdate.", 0.01)
        elif c == '5':
            data = _read("data/mahasiswa.txt")
            q = input("Cari NIM/nama: ").strip().lower()
            filtered = [m for m in data if q in str(m.get('nim','')).lower() or q in str(m.get('nama','')).lower()] if q else data
            print("Urutkan berdasarkan: 1=NIM 2=Nama 3=Kelas 4=Tanpa urut")
            s = input("Pilih: ").strip()
            if s == '1':
                filtered = sort_data(filtered, 'nim')
            elif s == '2':
                filtered = sort_data(filtered, 'nama')
            elif s == '3':
                filtered = sort_data(filtered, 'kelas')
            print("NIM | Nama | Kelas | Jurusan")
            for m in filtered:
                print(f"{m.get('nim')} | {m.get('nama')} | {m.get('kelas','-')} | {m.get('jurusan','-')}")
            pause()
        else:
            break

# ----------------------------
# 3. Kelola Dosen (buat akun + assign matkul)
# ----------------------------
def manage_dosen():
    while True:
        print("\n--- Kelola Dosen ---")
        print("1. Lihat Dosen")
        print("2. Tambah Dosen (lengkap & buat akun)")
        print("3. Hapus Dosen")
        print("4. Assign Mata Kuliah ke Dosen")
        print("5. Search & Sort Dosen")
        print("6. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            data = _read("data/dosen.txt")
            for d in data:
                print(f"- {d.get('id')} | {d.get('nama')} | Matkul: {d.get('matkul','-')}")
            pause()
        elif c == '2':
            did = input("ID Dosen unik: ").strip()
            nama = input("Nama: ").strip()
            matkul = input("Mata kuliah (pisah koma jika lebih): ").strip()  # store as CSV string
            pwd = input("Password (kosong untuk auto): ").strip()
            if not pwd:
                pwd = rand_password()
            _append("data/dosen.txt", {"id":did,"nama":nama,"matkul":matkul})
            append_user({"username":did,"password":pwd,"role":"dosen","identitas":did})
            typing(f"✔ Dosen & akun dibuat. Password: {pwd}", 0.01)
        elif c == '3':
            did = input("ID Dosen hapus: ").strip()
            data = _read("data/dosen.txt")
            data = [d for d in data if d.get("id") != did]
            _write("data/dosen.txt", data)
            users = _read("data/users.txt")
            users = [u for u in users if not (u.get("role")=="dosen" and u.get("identitas")==did)]
            _write("data/users.txt", users)
            typing("✔ Dosen dihapus.", 0.01)
        elif c == '4':
            did = input("ID Dosen: ").strip()
            kode = input("Kode matkul (pisah koma bila banyak): ").strip()
            dos = _read("data/dosen.txt")
            for d in dos:
                if d.get("id")==did:
                    cur = d.get("matkul","")
                    lst = [x.strip() for x in cur.split(",") if x.strip()] if cur else []
                    new = [x.strip() for x in kode.split(",") if x.strip()]
                    for k in new:
                        if k not in lst:
                            lst.append(k)
                    d["matkul"] = ",".join(lst)
            _write("data/dosen.txt", dos)
            typing("✔ Mata kuliah diassign ke dosen.", 0.01)
        elif c == '5':
            data = _read("data/dosen.txt")
            q = input("Cari ID/nama/matkul: ").strip().lower()
            filtered = [d for d in data if q in str(d.get('id','')).lower() or q in str(d.get('nama','')).lower() or q in str(d.get('matkul','')).lower()] if q else data
            print("Urutkan berdasarkan: 1=ID 2=Nama 3=Matkul 4=Tanpa urut")
            s = input("Pilih: ").strip()
            if s == '1':
                filtered = sort_data(filtered, 'id')
            elif s == '2':
                filtered = sort_data(filtered, 'nama')
            elif s == '3':
                filtered = sort_data(filtered, 'matkul')
            print("ID | Nama | Matkul")
            for d in filtered:
                print(f"{d.get('id')} | {d.get('nama')} | {d.get('matkul','-')}")
            pause()
        else:
            break

# ----------------------------
# 4. Mata Kuliah (master)
# ----------------------------
def manage_matkul():
    while True:
        print("\n--- Kelola Mata Kuliah ---")
        print("1. Lihat mata kuliah")
        print("2. Tambah mata kuliah")
        print("3. Hapus mata kuliah")
        print("4. Kelola Jadwal Mata Kuliah")
        print("5. Search & Sort Mata Kuliah")
        print("6. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            data = _read("data/matkul.txt")
            if not data:
                print("Belum ada data mata kuliah.")
            else:
                for m in data:
                    print(f"{m.get('kode', '-') } | {m.get('nama', '-')}")
            pause()
        elif c == '2':
            kode = input("Kode matkul: ").strip()
            nama = input("Nama matkul: ").strip()
            if not kode or not nama:
                print("Kode dan nama tidak boleh kosong.")
            else:
                _append("data/matkul.txt", {"kode": kode, "nama": nama})
                print("✅ Matkul ditambahkan.")
        elif c == '3':
            kode = input("Kode matkul yang dihapus: ").strip()
            data = _read("data/matkul.txt")
            new = [m for m in data if m.get('kode') != kode]
            _write("data/matkul.txt", new)
            print("✅ Matkul dihapus.")
        elif c == '4':
            manage_matkul_schedule()
        elif c == '5':
            data = _read("data/matkul.txt")
            q = input("Cari kode/nama: ").strip().lower()
            filtered = [m for m in data if q in str(m.get('kode','')).lower() or q in str(m.get('nama','')).lower()] if q else data
            print("Urutkan berdasarkan: 1=Kode 2=Nama 3=Tanpa urut")
            s = input("Pilih: ").strip()
            if s == '1':
                filtered = sort_data(filtered, 'kode')
            elif s == '2':
                filtered = sort_data(filtered, 'nama')
            print("Kode | Nama")
            for m in filtered:
                print(f"{m.get('kode')} | {m.get('nama')}")
            pause()
        else:
            break


def manage_matkul_schedule():
    """Submenu untuk admin membuat/lihat/hapus jadwal mata kuliah.
    Jadwal disimpan di data/matkul_schedule.txt dengan fields:
    {id, kode, nama, hari, jam, ruang, dosen_id}
    """
    while True:
        print("\n--- Kelola Jadwal Mata Kuliah ---")
        print("1. Lihat jadwal")
        print("2. Tambah jadwal")
        print("3. Hapus jadwal")
        print("4. Kembali")
        c = input("Pilih: ").strip()
        schedules = _read("data/matkul_schedule.txt")
        if c == '1':
            if not schedules:
                print("Belum ada jadwal terdaftar.")
            else:
                print("ID | Kode | Nama | Hari | Jam | Ruang | DosenID")
                for s in schedules:
                    print(f"{s.get('id')} | {s.get('kode','-')} | {s.get('nama','-')} | {s.get('hari','-')} | {s.get('jam','-')} | {s.get('ruang','-')} | {s.get('dosen_id','-')}")
            pause()
        elif c == '2':
            kode = input("Kode matkul (harus sesuai di master): ").strip()
            mats = _read("data/matkul.txt")
            if not any(m.get('kode') == kode for m in mats):
                yn = input("Kode tidak ditemukan di master. Tambah matkul baru? (y/n): ").strip().lower()
                if yn == 'y':
                    nama = input("Nama matkul: ").strip()
                    _append("data/matkul.txt", {"kode": kode, "nama": nama})
                else:
                    print("Batal menambah jadwal.")
                    continue
            nama = next((m.get('nama') for m in mats if m.get('kode') == kode), "")
            hari = input("Hari (mis. Senin/Selasa/Rabu/...): ").strip()
            jam = input("Jam (mis. 09:00-11:00): ").strip()
            ruang = input("Ruang (opsional): ").strip()
            dosen_id = input("ID Dosen pengampu (opsional): ").strip()
            sid = gen_id("SCH")
            append_txt_row("data/matkul_schedule.txt", {"id": sid, "kode": kode, "nama": nama, "hari": hari.lower(), "jam": jam, "ruang": ruang, "dosen_id": dosen_id})
            print("✅ Jadwal ditambahkan.")
        elif c == '3':
            hid = input("Masukkan schedule id untuk dihapus: ").strip()
            if not hid:
                continue
            new = [s for s in schedules if s.get('id') != hid]
            _write("data/matkul_schedule.txt", new)
            print("✅ Jadwal dihapus.")
        else:
            break

# ----------------------------
# 5. Nilai / Transkrip
# ----------------------------
def manage_nilai():
    while True:
        print("\n--- Kelola Nilai ---")
        print("1. Lihat nilai")
        print("2. Tambah nilai")
        print("3. Hapus nilai")
        print("4. Edit nilai")
        print("5. Generate transkrip per NIM (export)")
        print("6. Kembali")
        c = input("Pilih: ").strip()
        rows = _read("data/nilai.txt")
        if c == '1':
            for r in rows:
                print(f"{r.get('id')} | {r.get('nim')} | {r.get('matkul')} | {r.get('nilai')} | SKS:{r.get('sks','-')}")
            pause()
        elif c == '2':
            nid = gen_id("NIL")
            nim = input("NIM: ").strip()
            matkul = input("Kode matkul: ").strip()
            nilai = input("Nilai (angka 0-100): ").strip()
            sks = input("SKS: ").strip()
            semester = input("Semester: ").strip()
            _append("data/nilai.txt", {"id":nid,"nim":nim,"matkul":matkul,"nilai":nilai,"sks":sks,"semester":semester})
            typing("✔ Nilai ditambahkan.", 0.01)
        elif c == '3':
            nid = input("ID nilai hapus: ").strip()
            rows = [r for r in rows if r.get("id") != nid]
            _write("data/nilai.txt", rows)
            typing("✔ Dihapus.", 0.01)
        elif c == '4':
            nid = input("ID nilai edit: ").strip()
            for r in rows:
                if r.get("id") == nid:
                    print("Field: nim, matkul, nilai, sks, semester")
                    f = input("Field: ").strip()
                    if f in r:
                        r[f] = input("Nilai baru: ").strip()
            _write("data/nilai.txt", rows)
            typing("✔ Data nilai diupdate.", 0.01)
        elif c == '5':
            nim = input("NIM untuk transkrip: ").strip()
            allvals = [r for r in rows if r.get("nim")==nim]
            if not allvals:
                typing("⚠ Tidak ada data nilai.", 0.01); continue
            allvals = sort_data(allvals, "semester")
            s = f"=== TRANSKRIP {nim} ===\n"
            tot_sks = 0; tot_bobot = 0.0
            for v in allvals:
                s += f"{v.get('semester')} | {v.get('matkul')} | {v.get('nilai')} | SKS:{v.get('sks')}\n"
                try:
                    sks = float(v.get("sks",0)); val = float(v.get("nilai",0))
                    tot_sks += sks; tot_bobot += val * sks
                except: pass
            ipk = round(tot_bobot / tot_sks, 2) if tot_sks>0 else 0
            s += f"Total SKS: {tot_sks} | IPK: {ipk}\n"
            export_txt(f"exports/transkrip_{nim}.txt", s)
            typing("✔ Transkrip diexport ke folder exports.", 0.01)
        else:
            break

# ----------------------------
# 6. Tugas & Absensi
# ----------------------------
def manage_tugas_absensi():
    while True:
        print("\n--- Tugas & Absensi ---")
        print("1. Lihat tugas")
        print("2. Buat tugas")
        print("3. Edit tugas")
        print("4. Hapus tugas")
        print("5. Lihat absensi")
        print("6. Catat absensi")
        print("7. Edit absensi")
        print("8. Hapus absensi")
        print("9. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            for t in _read("data/tugas.txt"):
                print(f"{t.get('kode')} | {t.get('matkul')} | {t.get('judul')} | {t.get('status')}")
            pause()
        elif c == '2':
            kode = gen_id("TUG")
            matkul = input("Kode matkul: ").strip()
            judul = input("Judul tugas: ").strip()
            desc = input("Deskripsi: ").strip()
            dl = input("Deadline (YYYY-MM-DD): ").strip()
            _append("data/tugas.txt", {"kode":kode,"matkul":matkul,"judul":judul,"deskripsi":desc,"deadline":dl,"status":"Belum"})
            typing("✔ Tugas dibuat.", 0.01)
        elif c == '3':
            tid = input("ID tugas edit: ").strip()
            rows = _read("data/tugas.txt")
            for t in rows:
                if t.get('kode') == tid:
                    print("Field: matkul, judul, deskripsi, deadline, status")
                    f = input("Field: ").strip()
                    if f in t:
                        t[f] = input("Nilai baru: ").strip()
            _write("data/tugas.txt", rows)
            typing("✔ Data tugas diupdate.", 0.01)
        elif c == '4':
            tid = input("ID tugas hapus: ").strip()
            rows = _read("data/tugas.txt")
            rows = [t for t in rows if t.get('kode') != tid]
            _write("data/tugas.txt", rows)
            typing("✔ Tugas dihapus.", 0.01)
        elif c == '5':
            for a in _read("data/absensi.txt"):
                print(f"{a.get('nim')} | {a.get('matkul')} | {a.get('tanggal')} | {a.get('status')}")
            pause()
        elif c == '6':
            nim = input("NIM: ").strip()
            matkul = input("Matkul: ").strip()
            tanggal = input("Tanggal (YYYY-MM-DD) [enter untuk hari ini]: ").strip()
            if not tanggal: tanggal = today()
            status = input("Status (Hadir/Izin/Alfa): ").strip()
            _append("data/absensi.txt", {"nim":nim,"matkul":matkul,"tanggal":tanggal,"status":status})
            typing("✔ Absensi dicatat.", 0.01)
        elif c == '7':
            aid = input("ID absensi edit: ").strip()
            rows = _read("data/absensi.txt")
            for a in rows:
                if a.get('nim') == aid:
                    print("Field: matkul, tanggal, status")
                    f = input("Field: ").strip()
                    if f in a:
                        a[f] = input("Nilai baru: ").strip()
            _write("data/absensi.txt", rows)
            typing("✔ Data absensi diupdate.", 0.01)
        elif c == '8':
            aid = input("ID absensi hapus (NIM): ").strip()
            rows = _read("data/absensi.txt")
            rows = [a for a in rows if a.get('nim') != aid]
            _write("data/absensi.txt", rows)
            typing("✔ Absensi dihapus.", 0.01)
        else:
            break

# ----------------------------
# 7. SPP / Pembayaran (dgn nominal)
# ----------------------------
def manage_spp():
    while True:
        print("\n--- SPP / Pembayaran ---")
        print("1. Lihat data SPP")
        print("2. Tambah tagihan")
        print("3. Catat pembayaran")
        print("4. Edit SPP")
        print("5. Hapus SPP")
        print("6. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            for s in _read("data/spp.txt"):
                print(f"{s.get('nim')} | Rp{s.get('nominal')} | Terbayar: Rp{s.get('terbayar',0)} | {s.get('status')}")
            pause()
        elif c == '2':
            nim = input("NIM: ").strip()
            nominal_str = input("Nominal (angka): Rp").strip()
            if not nominal_str:
                print("Nominal tidak boleh kosong."); continue
            try:
                nominal = float(nominal_str)
            except:
                print("Nominal harus angka."); continue
            _append("data/spp.txt", {"nim":nim,"nominal":nominal,"terbayar":0,"status":"Belum Lunas"})
            typing("✔ Tagihan SPP ditambahkan.", 0.01)
        elif c == '3':
            nim = input("NIM bayar: ").strip()
            amt_str = input("Jumlah bayar: Rp").strip()
            if not amt_str:
                print("Jumlah bayar tidak boleh kosong."); continue
            try:
                amt = float(amt_str)
            except:
                print("Jumlah bayar harus angka."); continue
            rows = _read("data/spp.txt")
            for r in rows:
                if r.get("nim")==nim:
                    r["terbayar"] = float(r.get("terbayar",0)) + amt
                    r["status"] = "Lunas" if float(r.get("terbayar",0)) >= float(r.get("nominal",0)) else "Belum Lunas"
            _write("data/spp.txt", rows)
            typing("✔ Pembayaran dicatat.", 0.01)
        elif c == '4':
            nim = input("NIM SPP edit: ").strip()
            rows = _read("data/spp.txt")
            for s in rows:
                if s.get('nim') == nim:
                    print("Field: nominal, terbayar, status")
                    f = input("Field: ").strip()
                    if f in s:
                        s[f] = input("Nilai baru: ").strip()
            _write("data/spp.txt", rows)
            typing("✔ Data SPP diupdate.", 0.01)
        elif c == '5':
            nim = input("NIM SPP hapus: ").strip()
            rows = _read("data/spp.txt")
            rows = [s for s in rows if s.get('nim') != nim]
            _write("data/spp.txt", rows)
            typing("✔ SPP dihapus.", 0.01)
        else:
            break

# ----------------------------
# 8. Bus tracking
# ----------------------------
def manage_bus():
    while True:
        print("\n--- Bus Tracking ---")
        print("1. Lihat rute")
        print("2. Tambah/ubah rute")
        print("3. Edit rute")
        print("4. Hapus rute")
        print("5. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            for b in _read("data/bus_routes.txt"):
                print(f"{b.get('id')} | {b.get('from')} -> {b.get('to')} | {b.get('departure')} | {b.get('arrival')} | {b.get('status')}")
            pause()
        elif c == '2':
            rid = gen_id("BUS")
            fr = input("From: ").strip(); to = input("To: ").strip()
            dep = input("Departure (HH:MM): ").strip(); arr = input("Arrival (HH:MM): ").strip()
            status = input("Status (OnTime/Delayed/Cancelled): ").strip()
            _append("data/bus_routes.txt", {"id":rid,"from":fr,"to":to,"departure":dep,"arrival":arr,"status":status})
            typing("✔ Rute ditambahkan.", 0.01)
        elif c == '3':
            bid = input("ID rute edit: ").strip()
            rows = _read("data/bus_routes.txt")
            for b in rows:
                if b.get('id') == bid:
                    print("Field: from, to, departure, arrival, status")
                    f = input("Field: ").strip()
                    if f in b:
                        b[f] = input("Nilai baru: ").strip()
            _write("data/bus_routes.txt", rows)
            typing("✔ Data rute diupdate.", 0.01)
        elif c == '4':
            bid = input("ID rute hapus: ").strip()
            rows = _read("data/bus_routes.txt"); rows = [r for r in rows if r.get("id")!=bid]; _write("data/bus_routes.txt", rows)
            typing("✔ Dihapus.", 0.01)
        else:
            break

# ----------------------------
# 9. E-Library (multi-field search)
# ----------------------------
def manage_elibrary():
    while True:
        print("\n--- E-Library ---")
        print("1. List buku")
        print("2. Tambah buku")
        print("3. Cari buku (multi-field)")
        print("4. Edit buku")
        print("5. Hapus buku")
        print("6. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            for b in _read("data/ebooks.txt"):
                print(f"{b.get('id')} | {b.get('judul')} | ISBN:{b.get('isbn','-')} | Call:{b.get('nomor_panggil','-')}")
            pause()
        elif c == '2':
            judul = input("Judul: ").strip(); penulis = input("Penulis: ").strip()
            isbn = input("ISBN: ").strip(); publikasi = input("Publikasi: ").strip()
            nomor_panggil = input("Nomor panggil: ").strip(); bahasa = input("Bahasa: ").strip()
            subjek = input("Subjek: ").strip(); edisi = input("Edisi: ").strip()
            _append("data/ebooks.txt", {
                "id":gen_id("BOOK"),
                "judul":judul,"penulis":penulis,"isbn":isbn,
                "publikasi":publikasi,"nomor_panggil":nomor_panggil,
                "bahasa":bahasa,"subjek":subjek,"edisi":edisi
            })
            typing("✔ Buku dan metadata tersimpan.", 0.01)
        elif c == '3':
            kw = input("Masukkan kata kunci pencarian: ").strip()
            keys = ["judul","penulis","isbn","nomor_panggil","subjek","bahasa","edisi","publikasi"]
            found = multisearch(_read("data/ebooks.txt"), keys, kw)
            if not found:
                typing("⚠ Tidak ditemukan hasil.", 0.01)
            else:
                for b in found:
                    print(f"Judul: {b.get('judul')} | Edisi: {b.get('edisi','-')} | Publikasi: {b.get('publikasi','-')} | ISBN: {b.get('isbn','-')}")
                    cols = [c for c in _read("data/ebook_collections.txt") if c.get("isbn")==b.get("isbn")]
                    for col in cols:
                        print(f"  - Barcode:{col.get('barcode')} | Lokasi:{col.get('lokasi')} | Akses:{col.get('akses')} | Status:{col.get('status')}")
            pause()
        elif c == '4':
            bid = input("ID buku edit: ").strip()
            rows = _read("data/ebooks.txt")
            for b in rows:
                if b.get('id') == bid:
                    print("Field: judul, penulis, isbn, publikasi, nomor_panggil, bahasa, subjek, edisi")
                    f = input("Field: ").strip()
                    if f in b:
                        b[f] = input("Nilai baru: ").strip()
            _write("data/ebooks.txt", rows)
            typing("✔ Data buku diupdate.", 0.01)
        elif c == '5':
            bid = input("ID buku hapus: ").strip()
            rows = _read("data/ebooks.txt")
            rows = [b for b in rows if b.get('id') != bid]
            _write("data/ebooks.txt", rows)
            typing("✔ Buku dihapus.", 0.01)
        else:
            break

# ----------------------------
# 10. Notifications
# ----------------------------
def manage_notifications():
    while True:
        print("\n--- Pengumuman / Notifikasi ---")
        print("1. Lihat notifikasi")
        print("2. Buat notifikasi")
        print("3. Edit notifikasi")
        print("4. Hapus notifikasi")
        print("5. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            for n in _read("data/notifications.txt"):
                print(f"{n.get('tanggal')} | {n.get('role')} | {n.get('pesan')}")
            pause()
        elif c == '2':
            print("Tujuan: 1=Mahasiswa,2=Dosen,3=Semua")
            t = input("Pilih: ").strip()
            role = "all" if t=="3" else ("mahasiswa" if t=="1" else "dosen")
            pesan = input("Isi notifikasi: ").strip()
            push_notification(role, pesan)
            typing("✔ Notifikasi dikirim.", 0.01)
        elif c == '3':
            nid = input("ID notifikasi edit: ").strip()
            rows = _read("data/notifications.txt")
            for n in rows:
                if n.get('id') == nid:
                    print("Field: role, pesan, tanggal")
                    f = input("Field: ").strip()
                    if f in n:
                        n[f] = input("Nilai baru: ").strip()
            _write("data/notifications.txt", rows)
            typing("✔ Data notifikasi diupdate.", 0.01)
        elif c == '4':
            nid = input("ID notifikasi hapus: ").strip()
            rows = _read("data/notifications.txt")
            rows = [n for n in rows if n.get('id') != nid]
            _write("data/notifications.txt", rows)
            typing("✔ Notifikasi dihapus.", 0.01)
        else:
            break

# ----------------------------
# 11. Export all data
# ----------------------------
def export_all_data():
    files = ["users.txt","mahasiswa.txt","dosen.txt","matkul.txt","nilai.txt","tugas.txt","absensi.txt","spp.txt","bus_routes.txt","ebooks.txt","ebook_collections.txt","notifications.txt"]
    content = "=== EXPORT DATA SINTAK ===\n\n"
    for fn in files:
        data = _read(f"data/{fn}")
        content += f"\n--- {fn} ---\n"
        for d in data:
            try:
                content += json.dumps(d, ensure_ascii=False) + "\n"
            except:
                content += str(d) + "\n"
    export_txt("exports/all_data.txt", content)
    pause()

# ----------------------------
# 11. Manajemen Grup Chat
# ----------------------------
def manage_chat_groups():
    while True:
        print("\n--- Manajemen Grup Chat ---")
        print("1. Lihat semua grup chat")
        print("2. Buat grup baru")
        print("3. Tambah anggota ke grup")
        print("4. Hapus anggota dari grup")
        print("5. Hapus grup")
        print("6. Lihat semua chat di grup (real-time)")
        print("7. Kembali")
        c = input("Pilih: ").strip()
        from modules.utils import read_txt, write_txt, append_txt, gen_id, pause, typing
        import time
        if c == '1':
            groups = read_txt('data/chat_groups.txt')
            if not groups:
                print("Belum ada grup.")
            else:
                for g in groups:
                    print(f"{g.get('id')} | {g.get('nama')} | Anggota: {', '.join(g.get('anggota',[]))}")
            pause()
        elif c == '2':
            nama = input("Nama grup: ").strip()
            if not nama:
                print("Nama grup tidak boleh kosong."); continue
            gid = gen_id('GRUP')
            append_txt('data/chat_groups.txt', {"id": gid, "nama": nama, "anggota": []})
            print(f"Grup {nama} dibuat.")
        elif c == '3':
            gid = input("ID grup: ").strip()
            user = input("Username anggota: ").strip()
            groups = read_txt('data/chat_groups.txt')
            for g in groups:
                if g.get('id') == gid:
                    if user not in g['anggota']:
                        g['anggota'].append(user)
            write_txt('data/chat_groups.txt', groups)
            print("Anggota ditambahkan.")
        elif c == '4':
            gid = input("ID grup: ").strip()
            user = input("Username anggota yang dihapus: ").strip()
            groups = read_txt('data/chat_groups.txt')
            for g in groups:
                if g.get('id') == gid:
                    if user in g['anggota']:
                        g['anggota'].remove(user)
            write_txt('data/chat_groups.txt', groups)
            print("Anggota dihapus.")
        elif c == '5':
            gid = input("ID grup hapus: ").strip()
            groups = read_txt('data/chat_groups.txt')
            groups = [g for g in groups if g.get('id') != gid]
            write_txt('data/chat_groups.txt', groups)
            print("Grup dihapus.")
        elif c == '6':
            gid = input("ID grup: ").strip()
            print(f"\n=== Grup Chat: {gid} ===")
            while True:
                chats = read_txt('data/chat_messages.txt')
                filtered = [c for c in chats if c.get('group_id') == gid]
                print("\n-----------------------------")
                for c in filtered[-20:]:
                    sender = c.get('sender')
                    msg = c.get('message')
                    ts = c.get('ts')
                    print(f"[{sender}] {ts}: {msg}")
                print("-----------------------------")
                cmd = input("Tekan Enter untuk refresh, /exit untuk keluar: ").strip()
                if cmd == '/exit':
                    break
                time.sleep(1)
        else:
            break

# EOF
