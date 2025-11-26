# modules/mahasiswa.py
"""
Mahasiswa panel (full, fixed)
Fitur:
1. Lihat Nilai & IPK
2. Lihat Tugas
3. Absensi (menu: Lihat Sesi & Cek-in, Rekap Absensi Saya, Konfirmasi Hadir)
4. Export Data Saya (txt)
5. Transkrip (print/export)
6. KRS / Perwalian (ajukan)
7. Bimbingan TA (ajukan)
8. Cek SPP / Cicilan
9. E-Library (search buku)
10. Bus Tracking (lihat rute/status)
11. Profil Saya
12. Notifikasi
13. Submit Tugas
14. Grup Chat Saya
15. Jadwal Mata Kuliah Hari Ini
16. Kembali
"""
import os
import json
from datetime import datetime
from modules.utils import (
    read_txt, write_txt, append_txt, append_txt_row,
    gen_id, today, typing, pause, sort_data, multisearch,
    export_txt, get_notifications_for
)

# ---------- Helpers ----------
def _now_iso():
    return datetime.now().isoformat(timespec='seconds')

def safe_read(path):
    """If file missing -> [], else return read_txt result but always list."""
    if not os.path.exists(path):
        return []
    try:
        data = read_txt(path) or []
        return data
    except Exception:
        # fallback: read raw file lines
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return [l.strip() for l in f if l.strip()]
        except:
            return []

def parse_pipe_line(line):
    parts = [p.strip() for p in line.split("|")]
    # heuristics for nilai line: nim|mata_kuliah|nilai|sks
    if len(parts) >= 3 and parts[2].replace('.','',1).isdigit():
        d = {}
        d["nim"] = parts[0]
        d["mata_kuliah"] = parts[1]
        d["nilai"] = parts[2]
        if len(parts) >= 4:
            d["sks"] = parts[3]
        return d
    # notifications-like: id|role|title|message|date
    if len(parts) >= 5:
        return {
            "id": parts[0],
            "role": parts[1],
            "title": parts[2],
            "message": parts[3],
            "date": parts[4]
        }
    # ebooks etc fallback
    return {"raw_parts": parts}

def ensure_dict(item):
    """Return dict representation for JSON-lines or pipe-lines or raw dicts."""
    if isinstance(item, dict):
        return item
    if isinstance(item, str):
        s = item.strip()
        # try JSON
        try:
            return json.loads(s)
        except Exception:
            # try pipe parse
            return parse_pipe_line(s)
    return {}

def normalize_field(d, candidates):
    """Return first non-empty candidate field from dict d."""
    if not isinstance(d, dict):
        return None
    for k in candidates:
        if k in d and d.get(k) not in (None, ""):
            return d.get(k)
    return None

def normalize_name(x):
    return str(x).strip() if x not in (None, "") else ""

# ---------- Display ----------
def header(title):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)

def small_line():
    print("-" * 60)

# ---------- Main menu ----------
def menu_mahasiswa(user):
    nim = user.get('identitas') or user.get('username')
    username = user.get('username') or nim
    while True:
        header(f"MAHASISWA PANEL | {username} (NIM: {nim})")
        print("1. Lihat Nilai & IPK")
        print("2. Lihat Tugas")
        print("3. Absensi")
        print("4. Export Data Saya (txt)")
        print("5. Transkrip (print/export)")
        print("6. KRS / Perwalian (ajukan)")
        print("7. Bimbingan TA (ajukan)")
        print("8. Cek SPP / Cicilan")
        print("9. E-Library (search buku)")
        print("10. Bus Tracking (lihat rute/status)")
        print("11. Profil Saya")
        print("12. Notifikasi")
        print("13. Submit Tugas")
        print("14. Grup Chat Saya")
        print("15. Jadwal Mata Kuliah Hari Ini")
        print("16. Kembali")
        small_line()
        pilih = input("Pilih menu: ").strip()
        if pilih == "1":
            lihat_nilai_dan_ipk(nim)
        elif pilih == "2":
            lihat_tugas(nim)
        elif pilih == "3":
            absensi_menu(nim)
        elif pilih == "4":
            export_data_saya(nim, username)
        elif pilih == "5":
            generate_transkrip(nim)
        elif pilih == "6":
            ajukan_krs(nim)
        elif pilih == "7":
            ajukan_bimbingan_ta(nim)
        elif pilih == "8":
            cek_spp(nim)
        elif pilih == "9":
            elibrary_search_interactive()
        elif pilih == "10":
            bus_tracking_view()
        elif pilih == "11":
            profil_saya(nim)
        elif pilih == "12":
            tampilkan_notifikasi({"role":"mahasiswa","identitas":nim})
        elif pilih == "13":
            submit_tugas_interactive(nim)
        elif pilih == "14":
            menu_chat_mahasiswa(nim)
        elif pilih == "15":
            lihat_jadwal_hari_ini_mahasiswa(nim)
        elif pilih == "16":
            typing("🔙 Kembali ke menu utama...", 0.01)
            break
        else:
            typing("❌ Pilihan tidak valid.", 0.02)
        pause()

# ---------- 1. Nilai & IPK ----------
def lihat_nilai_dan_ipk(nim):
    header("Lihat Nilai & IPK")
    rows = safe_read("data/nilai.txt")
    my = []
    for raw in rows:
        d = ensure_dict(raw)
        nim_field = normalize_field(d, ["nim"])
        if nim_field == nim:
            matkul = normalize_field(d, ["mata_kuliah","matkul"])
            nilai = d.get("nilai") if d.get("nilai") not in (None,"") else d.get("score")
            sks = d.get("sks") or 0
            semester = d.get("semester") or ""
            try:
                nilai_f = float(nilai) if nilai not in (None,"") else 0
            except:
                nilai_f = 0
            try:
                sks_f = float(sks)
            except:
                sks_f = 0
            my.append({"mata_kuliah": normalize_name(matkul), "nilai": nilai_f, "sks": sks_f, "semester": semester})
    if not my:
        typing("⚠️  Belum ada nilai untuk NIM ini.", 0.02)
        pause()
        return
    small_line()
    print("No. | Mata Kuliah                    | SKS | Nilai")
    small_line()
    total_sks = 0.0
    total_bobot = 0.0
    for i,r in enumerate(my,1):
        print(f"{i:>2}.  | {r['mata_kuliah'][:30]:<30} | {int(r['sks']):>3} | {r['nilai']:>5}")
        total_sks += r['sks']
        total_bobot += r['nilai'] * r['sks']
    small_line()
    ipk = round(total_bobot / total_sks, 2) if total_sks > 0 else 0
    print(f"Total SKS: {int(total_sks)}")
    print(f"IPK: {ipk}")
    small_line()
    input("Tekan Enter untuk kembali...")

# ---------- 2. Tugas ----------
def lihat_tugas(nim):
    header("Daftar Tugas (Semua Mata Kuliah)")
    raw = safe_read("data/tugas.txt")
    tugas_list = []
    for item in raw:
        d = ensure_dict(item)
        judul = normalize_field(d, ["judul","tugas","title"]) or "-"
        mk = normalize_field(d, ["mata_kuliah","matkul"]) or "-"
        deadline = d.get("deadline") or d.get("due") or "-"
        id_tugas = d.get("id_tugas") or d.get("id") or gen_id("TUG")
        deskripsi = d.get("deskripsi") or d.get("desc") or ""
        dosen_id = d.get("dosen_id") or d.get("dosen") or d.get("dosenId") or ""
        tugas_list.append({
            "id_tugas": id_tugas,
            "mata_kuliah": normalize_name(mk),
            "judul": judul,
            "deskripsi": deskripsi,
            "deadline": deadline,
            "dosen_id": dosen_id
        })
    if not tugas_list:
        typing("Belum ada tugas terdaftar.", 0.02)
        pause()
        return
    small_line()
    for i,t in enumerate(tugas_list,1):
        print(f"{i}. [{t.get('mata_kuliah') or '-'}] {t.get('judul')} (ID: {t.get('id_tugas')}) | Deadline: {t.get('deadline') or '-'}")
    small_line()
    input("Tekan Enter untuk kembali...")

# ---------- 3. ABSENSI MENU & HELPERS ----------
def absensi_menu(nim):
    """Menu khusus absensi untuk mahasiswa: lihat sesi & cek-in, rekap, konfirmasi hadir"""
    while True:
        header("ABSENSI - Menu Mahasiswa")
        print("1. Lihat Sesi Absensi & Cek-in")
        print("2. Rekap Absensi Saya")
        print("3. Konfirmasi Hadir (cepat)")
        print("4. Kembali")
        small_line()
        c = input("Pilih (1/2/3/4): ").strip()
        if c == "1":
            view_sessions_and_checkin(nim)
        elif c == "2":
            rekap_absensi(nim)
        elif c == "3":
            konfirmasi_hadir(nim)
        else:
            break
        pause()

def _load_sessions():
    """Load attendance sessions (support variations)"""
    sessions = []
    for p in ("data/attendance_sessions.txt", "data/attendance_sessions.json", "data/attendance.txt"):
        if os.path.exists(p):
            sessions = safe_read(p)
            break
    parsed = []
    for s in sessions:
        d = ensure_dict(s)
        parsed.append({
            "id": d.get("id") or d.get("session_id") or d.get("sess") or gen_id("ATT"),
            "mata_kuliah": normalize_field(d, ["mata_kuliah","matkul"]) or "-",
            "dosen_id": d.get("dosen_id") or d.get("dosen") or "-",
            "date": d.get("date") or d.get("tanggal") or d.get("created_at") or "-",
            "note": d.get("note") or d.get("keterangan") or ""
        })
    return parsed

def view_sessions_and_checkin(nim):
    """Tampilkan sesi absensi yang dibuat dosen, beri opsi cek-in (sama dengan sebelumnya tapi rapi)"""
    header("Sesi Absensi (Dosen)")
    sessions = _load_sessions()
    if not sessions:
        typing("Belum ada sesi absensi yang dibuat dosen.", 0.02)
        input("Tekan Enter untuk kembali...")
        return
    print("Daftar sesi absensi:")
    for s in sessions:
        print(f"- {s.get('id')} | {s.get('mata_kuliah')} | Tanggal: {s.get('date')} | Catatan: {s.get('note')}")
    small_line()
    sel = input("Masukkan ID sesi untuk cek-in (Enter = kembali): ").strip()
    if not sel:
        return
    chosen = next((x for x in sessions if str(x.get('id')) == sel), None)
    if not chosen:
        typing("ID sesi tidak ditemukan.", 0.02)
        return
    # cek apakah sudah ada record untuk nim pada session ini
    records = safe_read("data/attendance_records.txt")
    already = False
    for r in records:
        d = ensure_dict(r)
        if normalize_field(d, ["session_id","session"]) == str(chosen.get("id")) and normalize_field(d, ["nim"]) == nim:
            already = True
            break
    if already:
        typing("Anda sudah melakukan absensi untuk sesi ini.", 0.02)
        return
    status = input("Masukkan status (default 'Hadir'): ").strip() or "Hadir"
    keterangan = input("Keterangan (opsional): ").strip() or ""
    rid = gen_id("AR")
    append_txt_row("data/attendance_records.txt", {
        "id": rid,
        "session_id": chosen.get("id"),
        "nim": nim,
        "mata_kuliah": chosen.get("mata_kuliah"),
        "status": status,
        "keterangan": keterangan,
        "ts": _now_iso()
    })
    typing(f"✅ Absensi tersimpan untuk sesi {chosen.get('id')}.", 0.02)

def rekap_absensi(nim):
    """Tampilkan rekap dan ringkasan hadir/izin/alpha dari semua sumber."""
    header("Rekap Absensi Saya")
    records = []
    # gabungkan berbagai file yang mungkin
    for p in ("data/attendance_records.txt","data/absensi.txt","data/attendance.txt"):
        if os.path.exists(p):
            records.extend(safe_read(p))
    my_records = []
    for rr in records:
        d = ensure_dict(rr)
        if normalize_field(d, ["nim"]) == nim:
            mata = normalize_field(d, ["mata_kuliah","matkul"]) or "-"
            tanggal = normalize_field(d, ["tanggal","date","ts"]) or d.get("ts") or "-"
            status = normalize_field(d, ["status"]) or d.get("keterangan") or "-"
            keterangan = d.get("keterangan") or d.get("ket") or ""
            my_records.append({"mata_kuliah": normalize_name(mata), "tanggal": tanggal, "status": status, "keterangan": keterangan})
    if not my_records:
        typing("⚠️  Tidak ada catatan absensi untuk NIM ini.", 0.02)
        pause()
        return
    hadir = sum(1 for r in my_records if str(r.get("status","")).lower() == "hadir")
    izin  = sum(1 for r in my_records if "izin" in str(r.get("status","")).lower())
    alfa  = sum(1 for r in my_records if "alpha" in str(r.get("status","")).lower() or "alfa" in str(r.get("status","")).lower())
    print(f"Rekap: Hadir: {hadir} | Izin: {izin} | Alfa: {alfa}")
    small_line()
    # tampilkan record terbaru
    for r in my_records[-50:]:
        print(f"{r.get('tanggal') or '-'} | {r.get('mata_kuliah'):<20} | {r.get('status')} | {r.get('keterangan') or ''}")
    small_line()
    input("Tekan Enter untuk kembali...")

def konfirmasi_hadir(nim):
    """
    Quick 'Konfirmasi Hadir' flow:
    - Tampilkan sesi yang belum diabsen oleh mahasiswa (berdasarkan attendance_sessions dan attendance_records)
    - Pilih sesi -> tambahkan record 'Hadir'
    """
    header("Konfirmasi Hadir (Quick)")
    sessions = _load_sessions()
    records = safe_read("data/attendance_records.txt")
    pending = []
    for s in sessions:
        sid = str(s.get("id"))
        # cek apakah nim sudah ada di records for this session
        exists = False
        for r in records:
            d = ensure_dict(r)
            if normalize_field(d, ["session_id","session"]) == sid and normalize_field(d, ["nim"]) == nim:
                exists = True
                break
        if not exists:
            pending.append(s)
    if not pending:
        typing("Tidak ada sesi yang menunggu konfirmasi hadir Anda (semua sudah diabsen).", 0.02)
        return
    print("Sesi yang belum diabsen:")
    for i,s in enumerate(pending,1):
        print(f"{i}. {s.get('id')} | {s.get('mata_kuliah')} | Tanggal: {s.get('date')} | Catatan: {s.get('note')}")
    sel = input("Pilih nomor sesi untuk konfirmasi hadir (Enter = batal): ").strip()
    if not sel:
        return
    try:
        idx = int(sel)-1
        chosen = pending[idx]
    except:
        typing("Pilihan tidak valid.", 0.02)
        return
    # tambahkan record hadr
    rid = gen_id("AR")
    append_txt_row("data/attendance_records.txt", {
        "id": rid,
        "session_id": chosen.get("id"),
        "nim": nim,
        "mata_kuliah": chosen.get("mata_kuliah"),
        "status": "Hadir",
        "keterangan": "Konfirmasi hadir oleh mahasiswa",
        "ts": _now_iso()
    })
    typing(f"✅ Kehadiran dikonfirmasi untuk sesi {chosen.get('id')}.", 0.02)

# ---------- 4. Export Data Saya ----------
def export_data_saya(nim, username):
    header("Export Data Saya")
    profil = {}
    for raw in safe_read("data/mahasiswa.txt"):
        d = ensure_dict(raw)
        if normalize_field(d, ["nim"]) == nim:
            profil = d
            break
    nilai_rows = []
    for raw in safe_read("data/nilai.txt"):
        d = ensure_dict(raw)
        if normalize_field(d, ["nim"]) == nim:
            nilai_rows.append({
                "semester": d.get("semester",""),
                "mata_kuliah": normalize_field(d, ["mata_kuliah","matkul"]),
                "nilai": d.get("nilai") or "",
                "sks": d.get("sks") or ""
            })
    tugas_rows = []
    for raw in safe_read("data/tugas.txt"):
        d = ensure_dict(raw)
        tugas_rows.append({
            "id_tugas": d.get("id_tugas") or d.get("id") or "-",
            "mata_kuliah": normalize_field(d,["mata_kuliah","matkul"]),
            "judul": normalize_field(d,["judul","tugas"]) or "-",
            "deadline": d.get("deadline") or "-"
        })
    absensi_rows = []
    for raw in safe_read("data/attendance_records.txt") + safe_read("data/absensi.txt"):
        d = ensure_dict(raw)
        if normalize_field(d, ["nim"]) == nim:
            absensi_rows.append({
                "mata_kuliah": normalize_field(d,["mata_kuliah","matkul"]),
                "tanggal": normalize_field(d,["tanggal","date","ts"]),
                "status": normalize_field(d,["status"]) or d.get("keterangan") or "-"
            })
    s = f"=== LAPORAN MAHASISWA {nim} ===\nTanggal export: {today()}\n\n"
    s += "DATA PRIBADI:\n"
    if profil:
        for k,v in profil.items():
            s += f"{k}: {v}\n"
    else:
        s += "(profil tidak ditemukan)\n"
    s += "\nNILAI:\n"
    for r in nilai_rows:
        s += f"{r.get('semester','?')} | {r.get('mata_kuliah')} | {r.get('nilai')} | SKS:{r.get('sks')}\n"
    s += "\nTUGAS:\n"
    for r in tugas_rows:
        s += f"- {r.get('id_tugas')} | {r.get('mata_kuliah')} | {r.get('judul')} | {r.get('deadline')}\n"
    s += "\nABSENSI:\n"
    for r in absensi_rows:
        s += f"{r.get('tanggal')} | {r.get('mata_kuliah')} | {r.get('status')}\n"
    path = f"exports/laporan_{username}.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    export_txt(path, s)
    typing(f"✅ Laporan diexport: {path}", 0.02)
    input("Tekan Enter untuk kembali...")

# ---------- 5. Transkrip ----------
def generate_transkrip(nim):
    header("Generate Transkrip")
    rows = safe_read("data/nilai.txt")
    mine = []
    for raw in rows:
        d = ensure_dict(raw)
        if normalize_field(d, ["nim"]) == nim:
            nilai = d.get("nilai") or 0
            sks = d.get("sks") or 0
            try:
                nilai_f = float(nilai)
            except:
                nilai_f = 0
            try:
                sks_f = float(sks)
            except:
                sks_f = 0
            mine.append({
                "semester": d.get("semester") or "",
                "mata_kuliah": normalize_field(d, ["mata_kuliah","matkul"]),
                "nilai": nilai_f,
                "sks": sks_f
            })
    if not mine:
        typing("Tidak ada data nilai.", 0.02)
        pause()
        return
    sorted_rows = sorted(mine, key=lambda x: int(x.get("semester") or 0))
    s = f"=== TRANSKRIP {nim} ===\n"
    total_sks = 0.0
    total_bobot = 0.0
    for r in sorted_rows:
        s += f"{r.get('semester','?')} | {r.get('mata_kuliah')} | {r.get('nilai')} | SKS:{int(r.get('sks',0))}\n"
        total_sks += r.get('sks',0)
        total_bobot += r.get('sks',0) * r.get('nilai',0)
    ipk = round(total_bobot / total_sks, 2) if total_sks > 0 else 0
    s += f"\nTotal SKS: {int(total_sks)}\nIPK   : {ipk}\n"
    path = f"exports/transkrip_{nim}.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    export_txt(path, s)
    typing(f"📁 Transkrip sudah diexport: {path}", 0.02)
    print("\nPreview Transkrip:\n")
    print(s)
    input("Tekan Enter untuk kembali...")

# ---------- 6. KRS ----------
def ajukan_krs(nim):
    header("Pengajuan KRS / Perwalian")
    mk_list = input("Masukkan mata kuliah yang diajukan (pisah koma): ").strip()
    if not mk_list:
        typing("Batal. Tidak ada mata kuliah diajukan.", 0.02)
        pause()
        return
    rec = {
        "id": gen_id("KRS"),
        "nim": nim,
        "mata_kuliah": [m.strip() for m in mk_list.split(",")],
        "tanggal": today(),
        "status": "Diajukan"
    }
    append_txt("data/krs.txt", rec)
    typing("✅ Pengajuan KRS tersimpan. Menunggu persetujuan dosen/wali.", 0.02)
    pause()

# ---------- 7. Bimbingan TA ----------
def ajukan_bimbingan_ta(nim):
    header("Pengajuan Bimbingan Tugas Akhir")
    topik = input("Masukkan topik/judul singkat TA: ").strip()
    dosen = input("Masukkan ID dosen pembimbing yang diinginkan (opsional): ").strip()
    catatan = input("Catatan / ringkasan (opsional): ").strip()
    rec = {
        "id": gen_id("BIM"),
        "nim": nim,
        "topik": topik,
        "dosen_id": dosen or "",
        "catatan": catatan,
        "tanggal": today(),
        "status": "Menunggu"
    }
    append_txt("data/bimbingan.txt", rec)
    typing("✅ Permintaan bimbingan TA tersimpan. Cek status di menu dosen/wali.", 0.02)
    pause()

# ---------- 8. Cek SPP ----------
def cek_spp(nim):
    header("Cek SPP / Cicilan")
    rows = safe_read("data/spp.txt")
    matches = []
    for raw in rows:
        d = ensure_dict(raw)
        if normalize_field(d,["nim"]) == nim:
            matches.append(d)
    if not matches:
        typing("Tidak ada catatan SPP untuk NIM ini.", 0.02)
        pause()
        return
    for r in matches:
        print("-"*40)
        print(f"Tahun: {r.get('tahun','-')} | Nominal: {r.get('nominal', r.get('jumlah','-'))} | Terbayar: {r.get('terbayar','-')} | Status: {r.get('status','-')}")
    small_line()
    input("Tekan Enter untuk kembali...")

# ---------- 9. E-Library ----------
def elibrary_search_interactive():
    header("E-Library Search")
    books_raw = []
    if os.path.exists("data/ebooks.txt"):
        books_raw = safe_read("data/ebooks.txt")
    elif os.path.exists("data/buku.txt"):
        books_raw = safe_read("data/buku.txt")
    if not books_raw:
        typing("Perpustakaan kosong. Tidak ada data buku.", 0.02)
        pause()
        return
    books = [ensure_dict(b) for b in books_raw]
    print("Metode pencarian: 1) Judul 2) Pengarang 3) ISBN 4) Semua Kolom")
    m = input("Pilih metode (1/2/3/4): ").strip()
    keyword = input("Masukkan kata kunci pencarian: ").strip()
    keys_map = {
        "1": ["judul","title"],
        "2": ["pengarang","author"],
        "3": ["isbn"],
        "4": ["judul","pengarang","penerbit","subjek","nomor_panggil","isbn","bahasa","edisi"]
    }
    keys = keys_map.get(m, keys_map["4"])
    results = multisearch(books, keys, keyword)
    if not results:
        typing("🔎 Hasil pencarian: tidak ditemukan.", 0.02)
        pause()
        return
    print(f"Menemukan {len(results)} buku:")
    for b in results:
        print("-"*60)
        print(f"Judul: {b.get('judul') or b.get('title','-')}")
        print(f"Pengarang: {b.get('pengarang', b.get('author','-'))} | ISBN: {b.get('isbn','-')}")
        print(f"CallNo: {b.get('nomor_panggil', b.get('callno','-'))} | Bahasa: {b.get('bahasa','-')}")
    small_line()
    input("Tekan Enter untuk kembali...")

# ---------- 10. Bus Tracking ----------
def bus_tracking_view():
    header("Bus Tracking - Rute & Status")
    data = []
    possible = ["data/bus_routes.txt", "data/bus.txt", "data/bus_routes.json"]
    for p in possible:
        if os.path.exists(p):
            data = safe_read(p)
            break
    if not data:
        typing("Belum ada data rute bus.", 0.02)
        pause()
        return
    routes = []
    for raw in data:
        d = ensure_dict(raw)
        route = {}
        route["route_id"] = normalize_field(d, ["route_id","id"])
        route["from"] = normalize_field(d, ["from","origin","asal"])
        route["to"] = normalize_field(d, ["to","destination","tujuan"])
        route["departure"] = normalize_field(d, ["departure","departure_time","jam_berangkat"])
        route["arrival"] = normalize_field(d, ["arrival","arrival_time","jam_tiba"])
        route["status"] = normalize_field(d, ["status"]) or "-"
        routes.append(route)
    q = input("Cari rute (kosong = semua): ").strip()
    filtered = []
    if q:
        ql = q.lower()
        for r in routes:
            if (r.get("from") and ql in str(r.get("from")).lower()) or (r.get("to") and ql in str(r.get("to")).lower()) or (r.get("route_id") and ql in str(r.get("route_id")).lower()):
                filtered.append(r)
    else:
        filtered = routes
    if not filtered:
        typing("Tidak ada rute yang cocok.", 0.02)
        pause()
        return
    for r in filtered:
        print(f"- {r.get('route_id') or '-'} | {r.get('from') or '-'} -> {r.get('to') or '-'} | {r.get('departure') or '-'} - {r.get('arrival') or '-'} | status: {r.get('status')}")
    small_line()
    input("Tekan Enter untuk kembali...")

# ---------- 11. Profil ----------
def profil_saya(nim):
    header("Profil Saya")
    rows = safe_read("data/mahasiswa.txt")
    profil = None
    for raw in rows:
        d = ensure_dict(raw)
        if normalize_field(d,["nim"]) == nim:
            profil = d
            break
    if not profil:
        typing("Profil tidak ditemukan.", 0.02)
        pause()
        return
    for k,v in profil.items():
        print(f"{k}: {v}")
    small_line()
    input("Tekan Enter untuk kembali...")

# ---------- 12. Notifikasi ----------
def tampilkan_notifikasi(user):
    header("Notifikasi & Pengumuman")
    role = user.get("role") or "mahasiswa"
    nim = user.get("identitas")
    notes = []
    try:
        notes = get_notifications_for(role) or []
    except:
        notes = []
    if not notes:
        raw = safe_read("data/notifications.txt")
        for item in raw:
            d = ensure_dict(item)
            role_field = normalize_field(d, ["role","role_or_all"]) or ""
            msg = normalize_field(d, ["message","pesan","title","judul"]) or ""
            date = normalize_field(d, ["date","tanggal"]) or ""
            notes.append({"role": role_field, "pesan": msg, "tanggal": date, "nim": d.get("nim")})
    notes_show = [n for n in notes if n.get("role") in ("all", role, "") or n.get("nim") == nim]
    if not notes_show:
        typing("Belum ada notifikasi.", 0.02)
        pause()
        return
    for n in notes_show:
        date = n.get("tanggal") or n.get("date") or ""
        msg = n.get("pesan") or n.get("message") or n.get("title") or ""
        print(f"- [{date}] {msg}")
    small_line()
    input("Tekan Enter untuk kembali...")

# ---------- 13. Submit Tugas ----------
def submit_tugas_interactive(nim):
    header("Submit Tugas")
    tasks_raw = safe_read("data/tugas.txt")
    tasks = []
    for raw in tasks_raw:
        d = ensure_dict(raw)
        tasks.append({
            "id_tugas": d.get("id_tugas") or d.get("id") or gen_id("TUG"),
            "judul": normalize_field(d, ["judul","tugas"]) or "-",
            "mata_kuliah": normalize_field(d, ["mata_kuliah","matkul"]) or "-"
        })
    if not tasks:
        typing("Belum ada tugas yang tersedia.", 0.02)
        pause()
        return
    for i,t in enumerate(tasks,1):
        print(f"{i}. {t.get('mata_kuliah')} | {t.get('judul')} (ID: {t.get('id_tugas')})")
    sel = input("Pilih nomor tugas untuk submit (atau Enter untuk batal): ").strip()
    if not sel:
        return
    try:
        si = int(sel)-1
        task = tasks[si]
    except Exception:
        typing("Pilihan tidak valid.", 0.02)
        pause()
        return
    content = input("Ketik jawaban / catatan (atau path file): ").strip()
    sub_id = gen_id("SUB")
    append_txt_row("data/submissions.txt", {
        "id": sub_id,
        "tugas_id": task.get("id_tugas"),
        "nim": nim,
        "content": content,
        "submitted_at": _now_iso(),
        "grade": "",
        "graded_by": ""
    })
    append_txt_row("data/activity.txt", {"user": nim, "action": f"submit_tugas:{task.get('id_tugas')}", "ts": _now_iso()})
    typing("✅ Submission tersimpan.", 0.02)
    pause()

# ---------- 14. Grup Chat ----------
def menu_chat_mahasiswa(nim):
    header("Grup Chat Saya")
    groups = safe_read("data/chat_groups.txt")
    my_groups = []
    for raw in groups:
        g = ensure_dict(raw)
        anggota = g.get("anggota") or []
        if isinstance(anggota, str):
            anggota = [s.strip() for s in anggota.split(",") if s.strip()]
        if nim in anggota or g.get("owner") == nim:
            my_groups.append(g)
    if not my_groups:
        typing("Anda belum terdaftar di grup apapun.", 0.02)
        pause()
        return
    for i,g in enumerate(my_groups,1):
        print(f"{i}. {g.get('id')} | {g.get('nama')} | Anggota: {', '.join(g.get('anggota') or [])}")
    sel = input("Pilih grup (nomor) atau Enter untuk kembali: ").strip()
    if not sel:
        return
    try:
        gi = int(sel)-1
        group = my_groups[gi]
    except:
        typing("Pilihan tidak valid.", 0.02)
        pause()
        return
    while True:
        header(f"Grup: {group.get('nama')}")
        messages = safe_read("data/chat_messages.txt")
        msgs = [ensure_dict(m) for m in messages if ensure_dict(m).get("group_id") == group.get("id")]
        for m in msgs[-30:]:
            sender = m.get("sender")
            ts = m.get("ts") or m.get("time") or ""
            print(f"[{sender}] {ts}: {m.get('message')}")
        cmd = input("Ketik pesan (Enter refresh, /exit untuk keluar): ").strip()
        if cmd == "/exit":
            break
        if cmd:
            append_txt("data/chat_messages.txt", {"group_id": group.get("id"), "sender": nim, "message": cmd, "ts": _now_iso()})
            typing("Pesan dikirim...", 0.01)
        else:
            continue

# ---------- 15. Jadwal Mata Kuliah Hari Ini ----------
def lihat_jadwal_hari_ini_mahasiswa(nim):
    header("Jadwal Mata Kuliah Hari Ini")
    enrolled = []
    for raw in safe_read("data/krs.txt"):
        d = ensure_dict(raw)
        if normalize_field(d, ["nim"]) == nim:
            mk = d.get("mata_kuliah") or d.get("matkul")
            if isinstance(mk, list):
                enrolled.extend(mk)
            elif isinstance(mk, str):
                enrolled.extend([m.strip() for m in mk.split(",") if m.strip()])
    if not enrolled and os.path.exists("data/mahasiswa.txt"):
        for raw in safe_read("data/mahasiswa.txt"):
            d = ensure_dict(raw)
            if normalize_field(d, ["nim"]) == nim:
                mk = normalize_field(d, ["mata_kuliah","matkul","krs"])
                if isinstance(mk, list):
                    enrolled.extend(mk)
                elif isinstance(mk, str) and mk:
                    enrolled.extend([m.strip() for m in mk.split(",") if m.strip()])
                break
    if not enrolled:
        typing("Anda belum mengajukan / terdaftar di mata kuliah apapun (tidak ada data KRS).", 0.02)
        pause()
        return
    schedules = safe_read("data/matkul_schedule.txt")
    if not schedules:
        typing("Data jadwal (data/matkul_schedule.txt) kosong.", 0.02)
        pause()
        return
    weekday_idx = datetime.today().weekday()
    indon_days = ['senin','selasa','rabu','kamis','jumat','sabtu','minggu']
    today_indo = indon_days[weekday_idx]
    today_en = datetime.today().strftime('%A').lower()
    found = []
    for raw in schedules:
        s = ensure_dict(raw)
        hari = str(s.get("hari","")).lower()
        if not hari:
            continue
        if hari in (today_indo, today_en) or hari == str(weekday_idx) or hari == str(weekday_idx+1):
            kode = str(s.get("kode") or s.get("nama") or "").lower()
            nama = str(s.get("nama") or "").lower()
            for m in enrolled:
                if str(m).lower() in kode or str(m).lower() in nama or kode in str(m).lower():
                    found.append(s)
                    break
    if not found:
        typing("Tidak ada jadwal hari ini untuk matkul yang Anda ambil.", 0.02)
        pause()
        return
    print("\nJadwal Hari Ini:")
    for f in found:
        print(f"- {f.get('kode') or f.get('nama','-')} | {f.get('jam','-')} | Ruang: {f.get('ruang','-')} | Dosen: {f.get('dosen_id') or f.get('dosen','-')}")
    small_line()
    input("Tekan Enter untuk kembali...")

# ---------- wrapper pause ----------
def pause():
    try:
        from modules.utils import pause as _p
        _p()
    except Exception:
        input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    print("Module mahasiswa.py — import and call menu_mahasiswa(user) from main.")
