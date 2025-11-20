# modules/utils.py
import os
import sys
import json
import uuid
import time
from datetime import datetime

# ----------------------------
# Terminal effects
# ----------------------------
def typing(text, speed=0.01):
    """Animasi mengetik singkat"""
    for c in str(text):
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def pause(msg="\nTekan Enter untuk kembali..."):
    input(msg)

# ----------------------------
# Filesystem / DB: line-json per baris
# ----------------------------
def ensure_data_files():
    os.makedirs("data", exist_ok=True)
    os.makedirs("exports", exist_ok=True)

    files = {
        "data/users.txt": [],
        "data/mahasiswa.txt": [],
        "data/dosen.txt": [],
        "data/matkul.txt": [],            # daftar mata kuliah master
        "data/nilai.txt": [],
        "data/tugas.txt": [],
        "data/absensi.txt": [],
        "data/spp.txt": [],
        "data/bus_routes.txt": [],
        "data/ebooks.txt": [],
        "data/ebook_collections.txt": [],
        "data/notifications.txt": [],
        "data/krs.txt": [],
        "data/bimbingan.txt": [],
        "data/activity_log.txt": [],
        # additional files used by admin/dosen modules
        "data/matkul_schedule.txt": [],
        "data/attendance_sessions.txt": [],
        "data/attendance_records.txt": [],
        "data/submissions.txt": [],
        "data/activity.txt": [],
        "data/chat_groups.txt": [],
        "data/chat_messages.txt": []
    }

    for path, default in files.items():
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                for item in default:
                    f.write(json.dumps(item) + "\n")

def read_txt(path):
    data = []
    if not os.path.exists(path):
        return data
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                data.append(json.loads(ln))
            except:
                # tolerate legacy simple lines
                try:
                    data.append({"raw": ln})
                except:
                    pass
    return data

def write_txt(path, list_of_dict):
    with open(path, "w", encoding="utf-8") as f:
        for row in list_of_dict:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def append_txt(path, dict_data):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(dict_data, ensure_ascii=False) + "\n")

# compatibility alias (older code used append_txt_row)
def append_txt_row(path, data):
    append_txt(path, data)

# ----------------------------
# Searching & sorting
# ----------------------------
def search(records, key, keyword):
    keyword = str(keyword).lower()
    return [r for r in records if key in r and keyword in str(r.get(key,"")).lower()]

def multisearch(records, keys, keyword):
    keyword = str(keyword).lower()
    out = []
    for r in records:
        for k in keys:
            if k in r and keyword in str(r.get(k,"")).lower():
                out.append(r)
                break
    return out

def sort_data(records, key, reverse=False):
    try:
        return sorted(records, key=lambda x: x.get(key,""), reverse=reverse)
    except Exception:
        return records

# ----------------------------
# Auth / Users
# ----------------------------
def find_user(username, password):
    users = read_txt("data/users.txt")
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            return u
    return None

def user_exists(username):
    users = read_txt("data/users.txt")
    return any(u.get("username") == username for u in users)

def append_user(user_record):
    append_txt("data/users.txt", user_record)

# register mahasiswa only (ensures role fixed)
def register_student(nim, nama, password):
    if user_exists(nim):
        return False, "NIM sudah terdaftar."
    # add mahasiswa
    m = {
        "nim": nim,
        "nama": nama,
        "kelas": "",
        "jurusan": "",
        "hp": "",
        "email": "",
        "ttl": "",
        "jk": ""
    }
    append_txt("data/mahasiswa.txt", m)
    # add user
    append_user({"username": nim, "password": password, "role": "mahasiswa", "identitas": nim})
    return True, "Registrasi berhasil."

# ----------------------------
# Utility generators & time
# ----------------------------
def rand_password():
    return uuid.uuid4().hex[:8]

def gen_id(prefix="ID"):
    return prefix + "_" + uuid.uuid4().hex[:6]

def today():
    return datetime.now().strftime("%Y-%m-%d")

# ----------------------------
# Export
# ----------------------------
def export_txt(filename, content):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(content))
    typing(f"📁 File diexport → {filename}")

# ----------------------------
# Notifications & Activity log
# ----------------------------
def push_notification(role, message):
    n = {
        "id": gen_id("NOTIF"),
        "role": role,      # "mahasiswa"/"dosen"/"all"
        "pesan": message,
        "tanggal": today()
    }
    append_txt("data/notifications.txt", n)

def get_notifications_for(role):
    notes = read_txt("data/notifications.txt")
    return [n for n in notes if n.get("role") in (role, "all")]

def log_activity(username, action):
    rec = {
        "id": gen_id("ACT"),
        "username": username,
        "action": action,
        "ts": datetime.now().isoformat()
    }
    append_txt("data/activity_log.txt", rec)

def get_activity_for(username=None, limit=100):
    logs = read_txt("data/activity_log.txt")
    if username:
        logs = [l for l in logs if l.get("username")==username]
    return logs[-limit:]
