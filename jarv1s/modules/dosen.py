# modules/dosen.py
"""
Modules for Dosen (Lecturer) panel — full features:
A) Nilai: input, lihat, searching & sorting, export (only for matkul the lecturer teaches)
B) Tugas: create task, view tasks, view student submissions, grade submissions
C) Absensi: create attendance sessions, students submit attendance, lecturer view & edit records
D) Extra: activity log, today's schedule
Data files used (JSON-per-line):
- data/dosen.txt
- data/nilai.txt
- data/tugas.txt
- data/submissions.txt
- data/attendance_sessions.txt
- data/attendance_records.txt
- data/activity.txt
- data/matkul.txt
- (optional) data/dosen_matkul.txt, data/matkul_schedule.txt
"""
import os
from datetime import datetime
from modules.utils import (
    read_txt, write_txt, append_txt, append_txt_row,
    gen_id, today, export_txt, typing, pause,
    sort_data, multisearch, search
)

# ---------------------------
# Helper / utilities
# ---------------------------
def _now_iso():
    return datetime.now().isoformat(timespec='seconds')

def normalize_matkul_field(d):
    """Support different possible keys used for matkul in data/dosen.txt"""
    if not d:
        return []
    # prefer common keys
    for key in ("matkul", "mata_kuliah", "matakuliah"):
        if key in d and d.get(key) is not None:
            val = d.get(key)
            if isinstance(val, list):
                return [x.strip() for x in val if x]
            return [x.strip() for x in str(val).split(",") if x.strip()]
    # fallback
    return []

def allowed_matkul_for_dosen(id_dosen):
    """
    Return list of matkul codes/names the dosen is assigned to.
    Support various data shapes:
      - data/dosen.txt having field 'id' or 'id_dosen' or 'dosen_id' or 'identitas'
      - separate mapping file data/dosen_matkul.txt with {"dosen": "...", "matkul": "..."}
    """
    dosen_list = read_txt('data/dosen.txt')
    for d in dosen_list:
        did = d.get('id') or d.get('id_dosen') or d.get('dosen_id') or d.get('identitas') or d.get('username')
        if str(did) == str(id_dosen):
            return normalize_matkul_field(d)
    # mapping file fallback
    if os.path.exists('data/dosen_matkul.txt'):
        dm = read_txt('data/dosen_matkul.txt')
        assigned = [r.get('matkul') for r in dm if str(r.get('dosen')) == str(id_dosen)]
        return [m for m in assigned if m]
    return []

# ---------------------------
# MAIN MENU FOR DOSEN
# ---------------------------
def menu_dosen(user):
    id_dosen = user.get('identitas') or user.get('username')
    while True:
        print("\n" + "="*60)
        print(f"👨‍🏫 DOSEN PANEL  |  {user.get('username')}  |  ID: {id_dosen}")
        print("="*60)
        print("A. Nilai")
        print("B. Tugas & Submissions")
        print("C. Absensi")
        print("D. Activity & Jadwal")
        print("E. Grup Chat Matkul Saya")
        print("F. Export nilai saya")
        print("Q. Logout / Kembali")
        choice = input("Pilih menu (A/B/C/D/E/F/Q): ").strip().upper()
        if choice == 'A':
            menu_nilai(id_dosen)
        elif choice == 'B':
            menu_tugas(id_dosen)
        elif choice == 'C':
            menu_absensi(id_dosen)
        elif choice == 'D':
            menu_activity_and_schedule(id_dosen)
        elif choice == 'E':
            menu_chat_dosen(id_dosen)
        elif choice == 'F':
            export_nilai_dosen(id_dosen)
        elif choice == 'Q':
            typing("🔒 Keluar dari panel dosen...", 0.01)
            break
        else:
            print("Pilihan tidak valid.")

# ---------------------------
# A) NILAI
# ---------------------------
def menu_nilai(id_dosen):
    while True:
        print("\n--- NILAI ---")
        print("1. Input Nilai Mahasiswa")
        print("2. Lihat Nilai Kelas (search & sort)")
        print("3. Export Nilai (txt)")
        print("4. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            input_nilai(id_dosen)
        elif c == '2':
            lihat_nilai_kelas(id_dosen)
        elif c == '3':
            export_nilai_dosen(id_dosen)
        else:
            break

def input_nilai(id_dosen):
    allowed = allowed_matkul_for_dosen(id_dosen)
    if not allowed:
        print("⚠ Anda belum terdaftar sebagai pengampu mata kuliah. Hubungi admin.")
        return
    print("Mata kuliah yang diampu:", ", ".join(allowed))
    mk = input("Mata Kuliah (ketik kode/nama persis): ").strip()
    if mk not in allowed:
        print("❌ Anda tidak diizinkan memasukkan nilai untuk mata kuliah ini.")
        return
    nim = input("NIM Mahasiswa: ").strip()
    if not nim:
        print("NIM tidak boleh kosong.")
        return
    nilai = input("Nilai (angka 0-100): ").strip()
    sks = input("SKS (mis. 3): ").strip() or "0"
    semester = input("Semester (mis. 1): ").strip() or "0"
    try:
        float(nilai)
    except:
        print("Nilai harus angka.")
        return
    nid = gen_id("NIL")
    append_txt_row('data/nilai.txt', {
        "id": nid,
        "nim": nim,
        "mata_kuliah": mk,
        "nilai": str(nilai),
        "sks": str(sks),
        "semester": str(semester),
        "input_by": id_dosen,
        "timestamp": _now_iso()
    })
    print(f"✅ Nilai tersimpan (ID: {nid}).")

def lihat_nilai_kelas(id_dosen):
    """
    Lihat Nilai Kelas dengan opsi searching & sorting.
    Searching: by NIM or by Mata Kuliah
    Sorting: nilai desc/asc, nim asc
    """
    allowed = allowed_matkul_for_dosen(id_dosen)
    if not allowed:
        print("⚠ Anda belum mengampu mata kuliah apapun.")
        return
    rows = read_txt('data/nilai.txt')
    if not rows:
        print("Belum ada data nilai.")
        return

    print("Mode tampil:")
    print("1. Semua nilai untuk matkul yang saya ampu")
    print("2. Search berdasarkan NIM")
    print("3. Search berdasarkan Mata Kuliah")
    mode = input("Pilih (1/2/3): ").strip()
    filtered = []
    if mode == '2':
        nim = input("Masukkan NIM: ").strip()
        filtered = [r for r in rows if r.get('nim') == nim and r.get('mata_kuliah') in allowed]
    elif mode == '3':
        mk = input("Masukkan mata kuliah: ").strip()
        if mk not in allowed:
            print("Mata kuliah tidak ada di daftar Anda.")
            return
        filtered = [r for r in rows if r.get('mata_kuliah') == mk]
    else:
        filtered = [r for r in rows if r.get('mata_kuliah') in allowed]

    if not filtered:
        print("Tidak ada data sesuai kriteria.")
        return

    # Sorting options
    print("\nOpsi sorting:")
    print("1. Nilai (Tertinggi -> Terendah)")
    print("2. Nilai (Terendah -> Tertinggi)")
    print("3. NIM (A->Z)")
    print("4. Tanpa urut")
    s = input("Pilih sorting (1/2/3/4): ").strip()
    try:
        if s == '1':
            filtered.sort(key=lambda x: float(x.get('nilai') or 0), reverse=True)
        elif s == '2':
            filtered.sort(key=lambda x: float(x.get('nilai') or 0))
        elif s == '3':
            filtered.sort(key=lambda x: x.get('nim') or "")
    except Exception as e:
        print("⚠ Warning: sorting gagal:", e)

    # Display
    print("\nNo | NIM       | Mata Kuliah           | SKS | Nilai | Semester | InputBy")
    print("-"*80)
    for i, r in enumerate(filtered, 1):
        print(f"{i:2d} | {r.get('nim',''):<9} | {r.get('mata_kuliah','')[:20]:<20} | {r.get('sks',''):<3} | {r.get('nilai',''):<5} | {r.get('semester',''):<3} | {r.get('input_by','')}")
    # Stats
    try:
        nums = [float(r.get('nilai')) for r in filtered if r.get('nilai') not in (None,"")]
        if nums:
            print(f"\nRata-rata kelas: {round(sum(nums)/len(nums),2)} | Count: {len(nums)}")
    except:
        pass
    pause()

def export_nilai_dosen(id_dosen):
    allowed = allowed_matkul_for_dosen(id_dosen)
    rows = read_txt('data/nilai.txt')
    out_lines = []
    for r in rows:
        if r.get('mata_kuliah') in allowed:
            out_lines.append(f"{r.get('nim')} | {r.get('mata_kuliah')} | {r.get('nilai')} | SKS:{r.get('sks')} | sem:{r.get('semester')}")
    if not out_lines:
        print("Tidak ada nilai untuk diexport.")
        return
    s = f"=== LAPORAN NILAI DOSEN {id_dosen} ===\n" + "\n".join(out_lines) + "\n"
    path = f"exports/laporan_nilai_{id_dosen}.txt"
    export_txt(path, s)
    print(f"✅ Export selesai → {path}")

# ---------------------------
# B) TUGAS & SUBMISSIONS
# ---------------------------
def menu_tugas(id_dosen):
    while True:
        print("\n--- TUGAS & SUBMISSION ---")
        print("1. Buat Tugas")
        print("2. Lihat Tugas (yang saya buat / untuk matkul saya)")
        print("3. Lihat Submission Mahasiswa untuk Tugas")
        print("4. Nilai Submission Mahasiswa")
        print("5. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            buat_tugas(id_dosen)
        elif c == '2':
            list_tugas_dosen(id_dosen)
        elif c == '3':
            lihat_submissions_for_tugas(id_dosen)
        elif c == '4':
            grade_submission(id_dosen)
        else:
            break

def buat_tugas(id_dosen):
    allowed = allowed_matkul_for_dosen(id_dosen)
    if not allowed:
        print("Anda belum mengampu matkul apapun.")
        return
    print("Mata kuliah Anda:", ", ".join(allowed))
    mk = input("Pilih mata kuliah (ketik persis): ").strip()
    if mk not in allowed:
        print("Tidak diizinkan.")
        return
    judul = input("Judul tugas: ").strip()
    deskripsi = input("Deskripsi singkat: ").strip()
    deadline = input("Deadline (YYYY-MM-DD): ").strip()
    task_id = gen_id("TUG")
    append_txt_row('data/tugas.txt', {
        "id_tugas": task_id,
        "mata_kuliah": mk,
        "dosen_id": id_dosen,
        "judul": judul,
        "deskripsi": deskripsi,
        "deadline": deadline,
        "created_at": _now_iso()
    })
    print(f"✅ Tugas dibuat (ID: {task_id}).")

def list_tugas_dosen(id_dosen):
    tasks = read_txt('data/tugas.txt')
    my_tasks = [t for t in tasks if str(t.get('dosen_id')) == str(id_dosen) or t.get('mata_kuliah') in allowed_matkul_for_dosen(id_dosen)]
    if not my_tasks:
        print("Tidak ada tugas terkait Anda.")
        return
    print("\nID | MataKuliah | Judul | Deadline | Created")
    for t in my_tasks:
        print(f"{t.get('id_tugas')} | {t.get('mata_kuliah')} | {t.get('judul')} | {t.get('deadline')} | {t.get('created_at','')}")
    q = input("Cari tugas (judul/matkul, kosong=skip): ").strip().lower()
    filtered = [t for t in my_tasks if q in str(t.get('judul','')).lower() or q in str(t.get('mata_kuliah','')).lower()] if q else my_tasks
    print("Urutkan: 1=Judul 2=MataKuliah 3=Deadline 4=Tanpa urut")
    s = input("Pilih: ").strip()
    if s == '1':
        filtered = sort_data(filtered, 'judul')
    elif s == '2':
        filtered = sort_data(filtered, 'mata_kuliah')
    elif s == '3':
        filtered = sort_data(filtered, 'deadline')
    print("ID | MataKuliah | Judul | Deadline | Created")
    for t in filtered:
        print(f"{t.get('id_tugas')} | {t.get('mata_kuliah')} | {t.get('judul')} | {t.get('deadline')} | {t.get('created_at','')}")
    pause()

def lihat_submissions_for_tugas(id_dosen):
    tasks = read_txt('data/tugas.txt')
    my_tasks = [t for t in tasks if str(t.get('dosen_id')) == str(id_dosen) or t.get('mata_kuliah') in allowed_matkul_for_dosen(id_dosen)]
    if not my_tasks:
        print("Tidak ada tugas.")
        return
    print("Tugas terdaftar (ID | Judul):")
    for t in my_tasks:
        print(f"- {t.get('id_tugas')} | {t.get('judul')}")
    tid = input("Masukkan ID tugas untuk melihat submission: ").strip()
    subs = read_txt('data/submissions.txt')
    found = [s for s in subs if s.get('tugas_id') == tid]
    if not found:
        print("Belum ada submission untuk tugas ini.")
        return
    # sort by timestamp
    found.sort(key=lambda x: x.get('submitted_at',''))
    print("\nNo | NIM | File/Text (preview) | Submitted At | Grade | GradedBy")
    for i, s in enumerate(found, 1):
        content = (s.get('content') or s.get('file') or "")[:60]
        print(f"{i:2d} | {s.get('nim')} | {content}{'...' if len(content)>=60 else ''} | {s.get('submitted_at')} | {s.get('grade','-')} | {s.get('graded_by','-')}")
    pause()

def grade_submission(id_dosen):
    tid = input("ID tugas: ").strip()
    subs = read_txt('data/submissions.txt')
    found = [s for s in subs if s.get('tugas_id') == tid]
    if not found:
        print("Tidak ada submission untuk tugas ini.")
        return
    print("Daftar submission (index | nim | submitted_at | grade)")
    for idx, s in enumerate(found, 1):
        print(f"{idx}. {s.get('nim')} | {s.get('submitted_at')} | grade: {s.get('grade','-')}")
    sel = input("Pilih index yang akan dinilai: ").strip()
    try:
        sel_i = int(sel)-1
        target = found[sel_i]
    except:
        print("Pilihan tidak valid.")
        return
    grade = input("Masukkan nilai tugas (angka): ").strip()
    comment = input("Komentar (opsional): ").strip()
    # update the submission in storage
    all_subs = read_txt('data/submissions.txt')
    for s in all_subs:
        if s.get('id') == target.get('id'):
            s['grade'] = grade
            s['graded_by'] = id_dosen
            s['graded_at'] = _now_iso()
            s['grader_comment'] = comment
    write_txt('data/submissions.txt', all_subs)
    print("✅ Submission dinilai dan disimpan.")

def student_submit_tugas(nim, tugas_id, content):
    """Used by mahasiswa module to submit tugas."""
    sid = gen_id("SUB")
    append_txt_row('data/submissions.txt', {
        "id": sid,
        "tugas_id": tugas_id,
        "nim": nim,
        "content": content,
        "submitted_at": _now_iso(),
        "grade": "",
        "graded_by": "",
        "graded_at": ""
    })
    append_txt_row('data/activity.txt', {
        "user": nim,
        "action": f"submit_tugas:{tugas_id}",
        "ts": _now_iso()
    })
    return sid

# ---------------------------
# C) ABSENSI
# ---------------------------
def menu_absensi(id_dosen):
    while True:
        print("\n--- ABSENSI ---")
        print("1. Buat sesi absensi (dosen)")
        print("2. Lihat sesi & hasil absen")
        print("3. Edit record absen")
        print("4. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            create_attendance_session(id_dosen)
        elif c == '2':
            view_attendance_results(id_dosen)
        elif c == '3':
            edit_attendance_record(id_dosen)
        else:
            break

def create_attendance_session(id_dosen):
    allowed = allowed_matkul_for_dosen(id_dosen)
    if not allowed:
        print("Anda belum mengampu matkul.")
        return
    print("Matkul:", ", ".join(allowed))
    mk = input("Mata kuliah: ").strip()
    if mk not in allowed:
        print("Tidak diizinkan.")
        return
    sess_id = gen_id("ATT")
    date_sess = input("Tanggal (YYYY-MM-DD, kosong = hari ini): ").strip()
    if not date_sess:
        date_sess = today()
    note = input("Catatan / lokasi (opsional): ").strip()
    append_txt_row('data/attendance_sessions.txt', {
        "id": sess_id,
        "mata_kuliah": mk,
        "dosen_id": id_dosen,
        "date": date_sess,
        "note": note,
        "created_at": _now_iso()
    })
    print(f"✅ Sesi absensi dibuat: {sess_id}")
    append_txt_row('data/activity.txt', {"user": id_dosen, "action": f"create_attendance:{sess_id}", "ts": _now_iso()})

def view_attendance_results(id_dosen):
    sessions = read_txt('data/attendance_sessions.txt')
    my_sessions = [s for s in sessions if s.get('dosen_id') == id_dosen or s.get('mata_kuliah') in allowed_matkul_for_dosen(id_dosen)]
    if not my_sessions:
        print("Tidak ada sesi absensi.")
        return
    for s in my_sessions:
        print(f"{s.get('id')} | {s.get('mata_kuliah')} | {s.get('date')} | {s.get('note')}")
    sid = input("Masukkan ID sesi untuk melihat records (kosong = kembali): ")

    if not sid:
        return
    records = read_txt('data/attendance_records.txt')
    # support keys variations: 'session_id' or 'session'
    recs = [r for r in records if r.get('session_id') == sid or r.get('session') == sid]
    if not recs:
        print("Belum ada record absen untuk sesi ini.")
        return
    print("\nNIM | Status | Timestamp | Keterangan")
    for r in recs:
        print(f"{r.get('nim')} | {r.get('status')} | {r.get('ts')} | {r.get('keterangan','')}")
    pause()

def edit_attendance_record(id_dosen):
    sid = input("Masukkan session_id: ").strip()
    if not sid:
        return
    recs = read_txt('data/attendance_records.txt')
    target = [r for r in recs if r.get('session_id') == sid or r.get('session') == sid]
    if not target:
        print("Tidak ada record.")
        return
    print("Daftar record (index | nim | status | ts):")
    for i, r in enumerate(target, 1):
        print(f"{i}. {r.get('nim')} | {r.get('status')} | {r.get('ts')}")
    sel = input("Pilih index untuk edit: ").strip()
    try:
        sel_i = int(sel)-1
        rec_to_edit = target[sel_i]
    except:
        print("Pilihan tidak valid.")
        return
    new_status = input(f"Masukkan status baru (sebelumnya: {rec_to_edit.get('status')}): ").strip()
    new_note = input("Keterangan baru (opsional): ").strip()
    all_recs = read_txt('data/attendance_records.txt')
    for r in all_recs:
        if r.get('id') == rec_to_edit.get('id'):
            r['status'] = new_status
            if new_note:
                r['keterangan'] = new_note
            r['edited_by'] = id_dosen
            r['edited_at'] = _now_iso()
    write_txt('data/attendance_records.txt', all_recs)
    print("✅ Record absen diperbarui.")

def student_mark_attendance(nim, session_id, status="Hadir", keterangan=""):
    """
    Called by mahasiswa when they 'cek in' attendance for a given session.
    Writes to data/attendance_records.txt and logs activity.
    """
    rid = gen_id("AR")
    append_txt_row('data/attendance_records.txt', {
        "id": rid,
        "session_id": session_id,
        "nim": nim,
        "status": status,
        "keterangan": keterangan,
        "ts": _now_iso()
    })
    append_txt_row('data/activity.txt', {"user": nim, "action": f"attendance:{session_id}:{status}", "ts": _now_iso()})
    return rid

# ---------------------------
# D) ACTIVITY & JADWAL
# ---------------------------
def menu_activity_and_schedule(id_dosen):
    while True:
        print("\n--- ACTIVITY & JADWAL ---")
        print("1. Lihat aktivitas mahasiswa (log)")
        print("2. Lihat jadwal matkul hari ini (dosen)")
        print("3. Lihat semua jadwal matkul saya")
        print("4. Lihat Notifikasi / Pengumuman")
        print("5. Proses KRS & Bimbingan TA Mahasiswa")
        print("6. Kembali")
        c = input("Pilih: ").strip()
        if c == '1':
            lihat_activity_logs()
        elif c == '2':
            lihat_jadwal_hari_ini(id_dosen)
        elif c == '3':
            lihat_semua_jadwal_dosen(id_dosen)
        elif c == '4':
            tampilkan_notifikasi_dosen(id_dosen)
        elif c == '5':
            proses_krs_bimbingan(id_dosen)
        else:
            break


def proses_krs_bimbingan(id_dosen):
    from modules.utils import read_txt, write_txt, push_notification, pause
    print("\n--- Proses KRS & Bimbingan TA Mahasiswa ---")
    print("1. KRS Mahasiswa")
    print("2. Bimbingan TA Mahasiswa")
    print("3. Kembali")
    c = input("Pilih: ").strip()
    if c == '1':
        krs = read_txt('data/krs.txt')
        pending = [r for r in krs if r.get('status') == 'Diajukan']
        if not pending:
            print("Tidak ada pengajuan KRS baru.")
            pause()
            return
        for idx, r in enumerate(pending, 1):
            print(f"{idx}. {r.get('nim')} | {r.get('mata_kuliah')} | {r.get('tanggal')}")
        sel = input("Pilih index untuk proses (kosong=batal): ").strip()
        if not sel:
            return
        try:
            sel_i = int(sel)-1
            target = pending[sel_i]
        except:
            print("Pilihan tidak valid.")
            return
        acc = input("Acc pengajuan KRS ini? (y/n): ").strip().lower()
        krs_all = read_txt('data/krs.txt')
        for r in krs_all:
            if r.get('id') == target.get('id'):
                r['status'] = 'Diterima' if acc == 'y' else 'Ditolak'
        write_txt('data/krs.txt', krs_all)
        push_notification('mahasiswa', f"Pengajuan KRS Anda ({target.get('nim')}) telah {'diterima' if acc == 'y' else 'ditolak'} oleh dosen.")
        print("Status KRS diupdate dan notifikasi dikirim.")
        pause()
    elif c == '2':
        bim = read_txt('data/bimbingan.txt')
        pending = [r for r in bim if r.get('status') == 'Menunggu']
        if not pending:
            print("Tidak ada permintaan bimbingan TA baru.")
            pause()
            return
        for idx, r in enumerate(pending, 1):
            print(f"{idx}. {r.get('nim')} | Topik: {r.get('topik')} | Dosen: {r.get('dosen_id')} | {r.get('tanggal')}")
        sel = input("Pilih index untuk proses (kosong=batal): ").strip()
        if not sel:
            return
        try:
            sel_i = int(sel)-1
            target = pending[sel_i]
        except:
            print("Pilihan tidak valid.")
            return
        acc = input("Acc permintaan bimbingan TA ini? (y/n): ").strip().lower()
        bim_all = read_txt('data/bimbingan.txt')
        for r in bim_all:
            if r.get('id') == target.get('id'):
                r['status'] = 'Diterima' if acc == 'y' else 'Ditolak'
        write_txt('data/bimbingan.txt', bim_all)
        push_notification('mahasiswa', f"Permintaan bimbingan TA Anda ({target.get('nim')}) telah {'diterima' if acc == 'y' else 'ditolak'} oleh dosen.")
        print("Status bimbingan TA diupdate dan notifikasi dikirim.")
        pause()
    else:
        return

def tampilkan_notifikasi_dosen(id_dosen):
    from modules.utils import get_notifications_for, typing, pause
    notes = get_notifications_for("dosen")
    if not notes:
        print("Tidak ada notifikasi/pengumuman untuk dosen.")
        pause()
        return
    print("\nNotifikasi / Pengumuman untuk Dosen:")
    for n in notes:
        print(f"[{n.get('tanggal','')}] {n.get('pesan','')}")
    pause()

def lihat_activity_logs():
    logs = read_txt('data/activity.txt')
    if not logs:
        print("Belum ada log aktivitas.")
        return
    q = input("Cari user/NIM (kosong = tampil semua): ").strip()
    results = logs
    if q:
        results = [l for l in logs if q in (l.get('user') or "") or q in (l.get('action') or "")]
    results.sort(key=lambda x: x.get('ts') or "")
    print("\nTS | USER | ACTION")
    for l in results[-200:]:
        print(f"{l.get('ts')} | {l.get('user')} | {l.get('action')}")
    pause()

def lihat_jadwal_hari_ini(id_dosen):
    my_matkul = allowed_matkul_for_dosen(id_dosen)
    if not my_matkul:
        print("Anda belum mengampu matkul apapun.")
        return
    schedules = []
    if os.path.exists('data/matkul_schedule.txt'):
        schedules = read_txt('data/matkul_schedule.txt')

    # Normalize today's day to Indonesian name and English name
    weekday_idx = datetime.today().weekday()  # 0=Mon .. 6=Sun
    indon_days = ['senin','selasa','rabu','kamis','jumat','sabtu','minggu']
    today_indo = indon_days[weekday_idx]
    today_en = datetime.today().strftime('%A').lower()

    def matkul_matches(s):
        # allow matching by kode or nama (case-insensitive)
        kode = str(s.get('kode') or '').lower()
        nama = str(s.get('nama') or '').lower()
        for m in my_matkul:
            if str(m).lower() in (kode, nama):
                return True
        return False

    found = []
    for s in schedules:
        hari_val = str(s.get('hari') or '').lower()
        if not hari_val:
            continue
        # accept several formats: indonesian day name, english day name, numeric (0-6 or 1-7)
        ok_day = False
        if hari_val in (today_indo, today_en):
            ok_day = True
        else:
            # check numeric day representations
            try:
                num = int(hari_val)
                if num == weekday_idx or num == (weekday_idx + 1):
                    ok_day = True
            except:
                pass
        if ok_day and matkul_matches(s):
            found.append(s)

    if not found:
        print("Tidak ada jadwal terdaftar untuk hari ini (atau data/matkul_schedule.txt kosong).")
        print("Matkul yang Anda ampu:", ", ".join(my_matkul))
        return
    print("\nJadwal Hari Ini:")
    for f in found:
        print(f"{f.get('kode')} | {f.get('nama','')} | {f.get('jam','-')} | Ruang: {f.get('ruang','-')} | Dosen: {f.get('dosen_id','-')}")
    pause()

def lihat_semua_jadwal_dosen(id_dosen):
    my_matkul = allowed_matkul_for_dosen(id_dosen)
    if not my_matkul:
        print("Anda belum mengampu matkul apapun.")
        pause()
        return
    schedules = []
    if os.path.exists('data/matkul_schedule.txt'):
        schedules = read_txt('data/matkul_schedule.txt')
    found = []
    for s in schedules:
        kode = str(s.get('kode') or '').lower()
        nama = str(s.get('nama') or '').lower()
        for m in my_matkul:
            if str(m).lower() in (kode, nama):
                found.append(s)
                break
    if not found:
        print("Tidak ada jadwal terdaftar untuk matkul Anda.")
        pause()
        return
    print("\nJadwal Semua Mata Kuliah yang Anda Ampu:")
    print("Hari | Jam | Kode | Nama | Ruang | DosenID")
    for f in found:
        print(f"{f.get('hari','-').capitalize()} | {f.get('jam','-')} | {f.get('kode','-')} | {f.get('nama','-')} | {f.get('ruang','-')} | {f.get('dosen_id','-')}")
    pause()

def menu_chat_dosen(id_dosen):
    from modules.utils import read_txt, write_txt, append_txt, gen_id, pause, typing
    import time
    print("\n--- Grup Chat Mata Kuliah Saya ---")
    groups = read_txt('data/chat_groups.txt')
    my_matkul = allowed_matkul_for_dosen(id_dosen)
    my_groups = [g for g in groups if g.get('nama') in my_matkul or id_dosen in g.get('anggota',[])]
    if not my_groups:
        print("Anda belum terdaftar di grup matkul apapun.")
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
            if sender == id_dosen:
                print(f"[Anda] {ts}: {msg}")
            else:
                print(f"[{sender}] {ts}: {msg}")
        print("-----------------------------")
        msg = input("Ketik pesan (Enter untuk refresh, /exit untuk keluar): ").strip()
        if msg == '/exit':
            break
        if msg:
            append_txt('data/chat_messages.txt', {"group_id": grup.get('id'), "sender": id_dosen, "message": msg, "ts": _now_iso()})
            typing("Pesan dikirim...", 0.01)
        else:
            time.sleep(1)
# ---------------------------
# If run as script for quick test
# ---------------------------
if __name__ == "__main__":
    print("Modul dosen.py — panggil menu_dosen(user) dari main.")
