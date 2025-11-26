# modules/utils.py
import os, sys, json, uuid, time
from datetime import datetime

# -------------------------
# Terminal effects / misc
# -------------------------
def typing(text, speed=0.002):
    for c in str(text):
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def pause(msg="\nTekan Enter untuk kembali..."):
    input(msg)

# -------------------------
# Files / DB (TXT, JSON-per-line)
# -------------------------
def ensure_data_files():
    os.makedirs("data", exist_ok=True)
    os.makedirs("exports", exist_ok=True)
    # list of needed files with empty default lists
    files = [
        "data/users.txt", "data/mahasiswa.txt", "data/dosen.txt",
        "data/matkul.txt", "data/nilai.txt", "data/tugas.txt",
        "data/submissions.txt", "data/attendance_sessions.txt",
        "data/attendance_records.txt", "data/activity.txt",
        "data/spp.txt", "data/bus_routes.txt", "data/ebooks.txt",
        "data/ebook_collections.txt", "data/notifications.txt",
        "data/krs.txt", "data/bimbingan.txt", "data/chat.txt",
        "data/dosen_matkul.txt", "data/matkul_schedule.txt"
    ]
    for p in files:
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                pass  # empty file

def read_txt(path):
    data = []
    if not os.path.exists(path):
        return data
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # tolerate both JSON-per-line and legacy pipe/raw lines
            try:
                obj = json.loads(line)
            except:
                # try to parse simple pipe header lines or fallback to raw
                try:
                    # if it looks like key|val|... ignore
                    if "|" in line and "{" not in line:
                        # skip header-like lines
                        continue
                    obj = json.loads(line.replace("'", '"'))
                except:
                    # last resort: store raw
                    obj = {"raw": line}
            data.append(obj)
    return data

def write_txt(path, list_of_dict):
    with open(path, "w", encoding="utf-8") as f:
        for row in list_of_dict:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def append_txt(path, dict_data):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(dict_data, ensure_ascii=False) + "\n")

# backward-compatible alias used in older modules
def append_txt_row(path, data):
    append_txt(path, data)

# -------------------------
# Search & Sort (level 2)
# -------------------------
def search(records, key, keyword):
    keyword = str(keyword).lower()
    return [r for r in records if key in r and keyword in str(r[key]).lower()]

def multisearch(records, keys, keyword):
    keyword = str(keyword).lower()
    out = []
    for r in records:
        for k in keys:
            if k in r and keyword in str(r[k]).lower():
                out.append(r)
                break
    return out

def sort_data(records, key, reverse=False):
    try:
        return sorted(records, key=lambda x: x.get(key, ""), reverse=reverse)
    except:
        return records

# -------------------------
# Auth
# -------------------------
def user_exists(username):
    users = read_txt("data/users.txt")
    return any(u.get("username") == username for u in users)

def find_user(username, password):
    users = read_txt("data/users.txt")
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            return u
    return None

def append_user(user_record):
    append_txt("data/users.txt", user_record)

# -------------------------
# Register student helper (registration only for mahasiswa)
# -------------------------
def register_student(nim, nama, password):
    if user_exists(nim):
        return False, "NIM sudah terdaftar sebagai akun."
    # add mahasiswa profile
    append_txt("data/mahasiswa.txt", {
        "nim": nim, "nama": nama, "kelas": "", "jurusan": ""
    })
    # add login user with role mahasiswa
    append_user({
        "username": nim,
        "password": password,
        "role": "mahasiswa",
        "identitas": nim
    })
    return True, "Registrasi mahasiswa berhasil."

# -------------------------
# Generator utils
# -------------------------
def rand_password():
    return uuid.uuid4().hex[:8]

def gen_id(prefix="ID"):
    return prefix + "_" + uuid.uuid4().hex[:6]

def today():
    return datetime.now().strftime("%Y-%m-%d")

# -------------------------
# Export helper
# -------------------------
def export_txt(filename, content):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    typing(f"📁 File berhasil diexport → {filename}")

# -------------------------
# Notifications
# -------------------------
def push_notification(role, message, title=None):
    rec = {
        "id": gen_id("NOTIF"),
        "role": role,
        "title": title or "",
        "pesan": message,
        "tanggal": today()
    }
    append_txt("data/notifications.txt", rec)

def get_notifications_for(role_or_user):
    notes = read_txt("data/notifications.txt")
    out = []
    for n in notes:
        # role could be "mahasiswa", "dosen", "admin" or "all"
        if n.get("role") in (role_or_user, "all") or n.get("nim") == role_or_user:
            out.append(n)
    return out

# -------------------------
# Shared student helpers (placed here to avoid circular imports)
# -------------------------
def student_submit_tugas(nim, tugas_id, content):
    sid = gen_id("SUB")
    append_txt("data/submissions.txt", {
        "id": sid,
        "tugas_id": tugas_id,
        "nim": nim,
        "content": content,
        "submitted_at": datetime.now().isoformat(timespec='seconds'),
        "grade": "",
        "graded_by": "",
    })
    # activity log
    append_txt("data/activity.txt", {
        "user": nim, "action": f"submit_tugas:{tugas_id}", "ts": datetime.now().isoformat(timespec='seconds')
    })
    return sid

def student_mark_attendance(nim, session_id, status="Hadir", keterangan=""):
    rid = gen_id("AR")
    append_txt("data/attendance_records.txt", {
        "id": rid,
        "session_id": session_id,
        "nim": nim,
        "status": status,
        "keterangan": keterangan,
        "ts": datetime.now().isoformat(timespec='seconds')
    })
    append_txt("data/activity.txt", {"user": nim, "action": f"attendance:{session_id}:{status}", "ts": datetime.now().isoformat(timespec='seconds')})
    return rid
