# modules/mahasiswa.py
import os
from datetime import datetime
from modules.utils import (
    read_txt, write_txt, append_txt, multisearch, sort_data,
    export_txt, gen_id, today, typing, pause, get_notifications_for, append_txt_row, push_notification
)

def header(title):
    os.system('cls' if os.name == 'nt' else 'clear')
    typing("=" * 60, 0.001)
    typing(f"🎓 {title}", 0.002)
    typing("=" * 60, 0.001)
    print()

def small_line():
    print("-" * 60)

def menu_mahasiswa(user):
    nim = user.get('identitas') or user.get('username')
    while True:
        header(f"MAHASISWA PANEL | {user.get('username')} (NIM: {nim})")
        typing("1. Lihat Nilai & IPK", 0.002)
        typing("2. Lihat Tugas", 0.002)
        typing("3. Lihat Absensi", 0.002)
        typing("4. Export Data Saya (txt)", 0.002)
        typing("5. Transkrip (print/export)", 0.002)
        typing("6. KRS / Perwalian (ajukan)", 0.002)
        typing("7. Bimbingan TA (ajukan)", 0.002)
        typing("8. Cek SPP / Cicilan", 0.002)
        typing("9. E-Library (search buku)", 0.002)
        typing("10. Bus Tracking (lihat rute/status)", 0.002)
        typing("11. Profil Saya", 0.002)
        typing("12. Notifikasi", 0.002)
        typing("13. Submit Tugas", 0.002)
        typing("14. Grup Chat Saya", 0.002)
        typing("15. Kembali", 0.002)
        print()
        pilih = input("Pilih menu: ").strip()
        if pilih == '1':
            lihat_nilai_dan_ipk(nim)
        elif pilih == '2':
            lihat_tugas(nim)
        elif pilih == '3':
            lihat_absensi(nim)
        elif pilih == '4':
            export_data_saya(nim, user.get('username'))
        elif pilih == '5':
            generate_transkrip(nim)
        elif pilih == '6':
            ajukan_krs(nim)
        elif pilih == '7':
            ajukan_bimbingan_ta(nim)
        elif pilih == '8':
            cek_spp(nim)
        elif pilih == '9':
            elibrary_search_interactive()
        elif pilih == '10':
            bus_tracking_view()
        elif pilih == '11':
            profil_saya(nim)
        elif pilih == '12':
            tampilkan_notifikasi(user)
        elif pilih == '13':
            submit_tugas_interactive(nim)
        elif pilih == '14':
            menu_chat_mahasiswa(nim)
        elif pilih == '15':
            typing("🔙 Kembali ke menu sebelumnya...", 0.02)
            break
        else:
            typing("❌ Pilihan tidak valid.", 0.02)
        pause()

def lihat_nilai_dan_ipk(nim):
    header("Lihat Nilai & IPK")
    nilai = read_txt("data/nilai.txt")
    my = [r for r in nilai if r.get("nim") == nim]
    if not my:
        typing("⚠️  Belum ada nilai untuk NIM ini.", 0.02)
        return
    small_line()
    print("No. | Mata Kuliah                    | SKS | Nilai")
    small_line()
    no = 1
    total_sks = 0.0
    total_bobot = 0.0
    for r in my:
        mk = r.get("mata_kuliah", "")
        sks = float(r.get("sks") or 0)
        val = float(r.get("nilai") or 0)
        print(f"{no:>2}.  | {mk:<30} | {int(sks):>3} | {val:>5}")
        total_sks += sks
        total_bobot += val * sks
        no += 1
    small_line()
    ipk = round(total_bobot / total_sks, 2) if total_sks > 0 else 0
    print(f"Total SKS: {int(total_sks)}")
    print(f"IPK: {ipk}")
    small_line()

def lihat_tugas(nim):
    header("Daftar Tugas (Semua Mata Kuliah)")
    tugas = read_txt("data/tugas.txt")
    if not tugas:
        typing("Belum ada tugas terdaftar.", 0.02)
        return
    q = input("Cari tugas (judul/matkul, kosong=skip): ").strip().lower()
    filtered = [t for t in tugas if q in str(t.get('judul','')).lower() or q in str(t.get('mata_kuliah','')).lower()] if q else tugas
    print("Urutkan: 1=Judul 2=MataKuliah 3=Deadline 4=Tanpa urut")
    s = input("Pilih: ").strip()
    if s == '1':
        filtered = sort_data(filtered, 'judul')
    elif s == '2':
        filtered = sort_data(filtered, 'mata_kuliah')
    elif s == '3':
        filtered = sort_data(filtered, 'deadline')
    for t in filtered:
        print(f"- ID:{t.get('id_tugas')} | {t.get('judul')} ({t.get('mata_kuliah')}) | Deadline: {t.get('deadline')}")
    small_line()

def lihat_absensi(nim):
    header("Rekap Absensi Saya")
    rows = read_txt("data/attendance_records.txt")
    hadir = sum(1 for r in rows if r.get("nim") == nim and r.get("status","").lower() == "hadir")
    izin = sum(1 for r in rows if r.get("nim") == nim and r.get("status","").lower() == "izin")
    alfa = sum(1 for r in rows if r.get("nim") == nim and r.get("status","").lower() == "alfa")
    print(f"Hadir : {hadir}")
    print(f"Izin  : {izin}")
    print(f"Alfa  : {alfa}")
    small_line()

def export_data_saya(nim, username):
    header("Export Data Saya")
    nilai = read_txt("data/nilai.txt")
    tugas = read_txt("data/tugas.txt")
    absn = read_txt("data/attendance_records.txt")
    mhs = read_txt("data/mahasiswa.txt")
    profile = next((m for m in mhs if m.get("nim")==nim), {})
    s = f"=== LAPORAN MAHASISWA {nim} ===\nTanggal export: {today()}\n\n"
    s += "DATA PRIBADI:\n"
    for k,v in profile.items():
        s += f"{k}: {v}\n"
    s += "\nNILAI:\n"
    for r in nilai:
        if r.get("nim") == nim:
            s += f"{r.get('semester','?')} | {r.get('mata_kuliah')} | {r.get('nilai')} | SKS:{r.get('sks')}\n"
    s += "\nTUGAS:\n"
    for r in tugas:
        s += f"- {r.get('id_tugas')} | {r.get('judul')} ({r.get('mata_kuliah')})\n"
    s += "\nABSENSI:\n"
    for r in absn:
        if r.get("nim") == nim:
            s += f"{r.get('ts','?')} | {r.get('mata_kuliah')} | {r.get('status')}\n"
    path = f"exports/laporan_{username}.txt"
    export_txt(path, s)
    typing(f"✅ Laporan diexport: {path}", 0.02)

def generate_transkrip(nim):
    header("Generate Transkrip")
    rows = read_txt("data/nilai.txt")
    mine = [r for r in rows if r.get("nim") == nim]
    if not mine:
        typing("Tidak ada data nilai.", 0.02)
        return
    sorted_rows = sort_data(mine, "semester", reverse=False)
    s = f"=== TRANSKRIP {nim} ===\n"
    total_sks = 0.0
    total_bobot = 0.0
    for r in sorted_rows:
        s += f"{r.get('semester','?')} | {r.get('mata_kuliah')} | {r.get('nilai')} | SKS:{r.get('sks')}\n"
        try:
            sks = float(r.get('sks') or 0)
            nilai = float(r.get('nilai') or 0)
            total_sks += sks
            total_bobot += sks * nilai
        except:
            pass
    ipk = round(total_bobot / total_sks, 2) if total_sks > 0 else 0
    s += f"\nTotal SKS: {int(total_sks)}\nIPK   : {ipk}\n"
    path = f"exports/transkrip_{nim}.txt"
    export_txt(path, s)
    typing(f"📁 Transkrip sudah diexport: {path}", 0.02)
    print("\nPreview Transkrip:\n")
    print(s)

def ajukan_krs(nim):
    header("Pengajuan KRS / Perwalian")
    mk_list = input("Masukkan mata kuliah yang diajukan (pisah koma): ").strip()
    if not mk_list:
        typing("Batal. Tidak ada mata kuliah diajukan.", 0.02)
        return
    mk_items = [m.strip() for m in mk_list.split(",") if m.strip()]
    if not mk_items:
        typing("Batal. Tidak ada mata kuliah valid.", 0.02)
        return
    record = {
        "id": gen_id("KRS"),
        "nim": nim,
        "mata_kuliah": mk_items,
        "tanggal": today(),
        "status": "Diajukan"
    }
    append_txt("data/krs.txt", record)
    typing("✅ Pengajuan KRS tersimpan. Menunggu persetujuan dosen/wali.", 0.02)
    from modules.utils import push_notification
    push_notification("dosen", f"Pengajuan KRS dari mahasiswa {nim}. Mohon review dan acc di menu dosen.")

def ajukan_bimbingan_ta(nim):
    header("Pengajuan Bimbingan Tugas Akhir")
    topik = input("Masukkan topik/judul singkat TA: ").strip()
    if not topik:
        typing("Batal. Topik tidak boleh kosong.", 0.02)
        return
    dosen = input("Masukkan ID dosen pembimbing yang diinginkan (opsional): ").strip()
    catatan = input("Catatan / ringkasan (opsional): ").strip()
    rec = {
        "id": gen_id("BIM"),
        "nim": nim,
        "topik": topik,
        "dosen_id": dosen or "-",
        "catatan": catatan,
        "tanggal": today(),
        "status": "Menunggu"
    }
    append_txt("data/bimbingan.txt", rec)
    typing("✅ Permintaan bimbingan TA tersimpan. Cek status di menu dosen/wali.", 0.02)
    from modules.utils import push_notification
    if dosen:
        push_notification("dosen", f"Permintaan bimbingan TA dari mahasiswa {nim} untuk dosen {dosen}. Mohon review di menu dosen.")
    else:
        push_notification("dosen", f"Permintaan bimbingan TA dari mahasiswa {nim}. Mohon review di menu dosen.")

def cek_spp(nim):
    header("Cek SPP / Cicilan")
    rows = read_txt("data/spp.txt")
    my = [r for r in rows if r.get("nim") == nim]
    if not my:
        typing("Tidak ada catatan SPP untuk NIM ini.", 0.02)
        return
    print("NIM | Nominal | Terbayar | Status")
    for r in my:
        print(f"{r.get('nim')} | Rp{r.get('nominal')} | Rp{r.get('terbayar',0)} | {r.get('status')}")
    small_line()

def elibrary_search_interactive():
    header("E-Library Search")
    books = read_txt("data/ebooks.txt")
    if not books:
        typing("Perpustakaan kosong. Tidak ada data buku.", 0.02)
        return
    typing("Metode pencarian: 1) Judul 2) Pengarang 3) ISBN 4) Semua Kolom", 0.01)
    m = input("Pilih metode (1/2/3/4): ").strip()
    keyword = input("Masukkan kata kunci pencarian: ").strip()
    keys_map = {
        "1": ["judul"],
        "2": ["penulis"],
        "3": ["isbn"],
        "4": ["judul","penulis","penerbit","subjek","nomor_panggil","isbn","bahasa"]
    }
    keys = keys_map.get(m, keys_map["4"])
    results = multisearch(books, keys, keyword)
    if not results:
        typing("🔎 Hasil pencarian: tidak ditemukan.", 0.02)
        return
    typing("Urutkan hasil? 1) Judul 2) Nomor panggil 3) Tidak perlu", 0.01)
    so = input("Pilih urutan (1/2/3): ").strip()
    if so == '1':
        results = sort_data(results, "judul")
    elif so == '2':
        results = sort_data(results, "nomor_panggil")
    small_line()
    for b in results:
        print(f"Judul   : {b.get('judul')}")
        print(f"Edisi   : {b.get('edisi','-')} | Publikasi: {b.get('publikasi','-')} | ISBN: {b.get('isbn','-')}")
        print(f"Call No : {b.get('nomor_panggil','-')} | Bahasa: {b.get('bahasa','-')} | Subjek: {b.get('subjek','-')}")
        cols = read_txt("data/ebook_collections.txt")
        for c in cols:
            if c.get("isbn") == b.get("isbn"):
                print(f"  * Barcode:{c.get('barcode')} | Lokasi:{c.get('lokasi')} | Akses:{c.get('akses')} | Status:{c.get('status')}")
        small_line()

def bus_tracking_view():
    header("Bus Tracking - Rute & Status")
    rows = read_txt("data/bus_routes.txt")
    if not rows:
        typing("Belum ada data rute bus.", 0.02)
        return
    q = input("Cari rute (kota/from/to) atau tekan Enter untuk tampil semua: ").strip()
    if q:
        filtered = []
        for r in rows:
            if q.lower() in str(r.get("from","")).lower() or q.lower() in str(r.get("to","")).lower():
                filtered.append(r)
    else:
        filtered = rows
    filtered = sort_data(filtered, "departure_time")
    for r in filtered:
        print(f"- {r.get('route_id')} | {r.get('from')} -> {r.get('to')} | {r.get('departure_time')} - {r.get('arrival_time')} | status: {r.get('status')}")
    small_line()

def profil_saya(nim):
    header("Profil Saya")
    rows = read_txt("data/mahasiswa.txt")
    me = next((r for r in rows if r.get("nim") == nim), None)
    if not me:
        typing("Profil tidak ditemukan.", 0.02)
        return
    for k,v in me.items():
        print(f"{k}: {v}")
    small_line()

def tampilkan_notifikasi(user):
    header("Notifikasi & Pengumuman")
    role = user.get("role") or "mahasiswa"
    notes = get_notifications_for(role)
    if not notes:
        typing("Belum ada notifikasi.", 0.02)
        return
    for n in notes:
        print(f"- [{n.get('tanggal')}] {n.get('pesan')}")
    small_line()

def submit_tugas_interactive(nim):
    tasks = read_txt("data/tugas.txt")
    if not tasks:
        typing("Belum ada tugas tersedia.", 0.02)
        return
    print("Tugas tersedia:")
    for t in tasks:
        print(f"- ID: {t.get('id_tugas')} | MK: {t.get('mata_kuliah')} | {t.get('judul')} | Deadline: {t.get('deadline')}")
    tid = input("Masukkan ID tugas yang akan dikumpulkan: ").strip()
    content = input("Masukkan jawaban (teks) atau path file (opsional): ").strip()
    sid = gen_id("SUB")
    append_txt_row("data/submissions.txt", {
        "id": sid,
        "tugas_id": tid,
        "nim": nim,
        "content": content,
        "submitted_at": datetime.now().isoformat(timespec='seconds'),
        "grade": "",
        "graded_by": "",
        "graded_at": ""
    })
    append_txt_row("data/activity.txt", {"user": nim, "action": f"submit_tugas:{tid}", "ts": datetime.now().isoformat(timespec='seconds')})
    typing(f"✅ Submission tersimpan (ID: {sid})", 0.02)

def menu_chat_mahasiswa(nim):
    from modules.utils import read_txt, write_txt, append_txt, gen_id, pause, typing
    import time
    print("\n--- Grup Chat Saya ---")
    groups = read_txt('data/chat_groups.txt')
    my_groups = [g for g in groups if nim in g.get('anggota',[])]
    if not my_groups:
        print("Anda belum terdaftar di grup apapun.")
        pause()
        return
    for idx, g in enumerate(my_groups, 1):
        print(f"{idx}. {g.get('id')} | {g.get('nama')} | Anggota: {', '.join(g.get('anggota',[]))}")
    sel = input("Pilih index grup untuk chat (kosong=batal): ").strip()
    if not sel:
        return
    try:
        sel_i = int(sel)-1
        grup = my_groups[sel_i]
    except:
        print("Pilihan tidak valid.")
        return
    print(f"\n=== Grup Chat: {grup.get('nama')} ===")
    while True:
        chats = read_txt('data/chat_messages.txt')
        filtered = [c for c in chats if c.get('group_id') == grup.get('id')]
        print("\n-----------------------------")
        for c in filtered[-20:]:
            sender = c.get('sender')
            msg = c.get('message')
            ts = c.get('ts')
            if sender == nim:
                print(f"[Anda] {ts}: {msg}")
            else:
                print(f"[{sender}] {ts}: {msg}")
        print("-----------------------------")
        msg = input("Ketik pesan (Enter untuk refresh, /exit untuk keluar): ").strip()
        if msg == '/exit':
            break
        if msg:
            append_txt('data/chat_messages.txt', {"group_id": grup.get('id'), "sender": nim, "message": msg, "ts": datetime.now().isoformat(timespec='seconds')})
            typing("Pesan dikirim...", 0.01)
        else:
            time.sleep(1)
