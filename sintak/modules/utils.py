# modules/utils.py
import csv
import os

def ensure_data_files():
    os.makedirs('data', exist_ok=True)
    os.makedirs('exports', exist_ok=True)

    # default files with header if not exist
    files = {
        'data/users.csv': ['username','password','role','identitas'],
        'data/mahasiswa.csv': ['nim','nama','kelas','jurusan'],
        'data/dosen.csv': ['id_dosen','nama_dosen','mata_kuliah'],
        'data/nilai.csv': ['nim','mata_kuliah','nilai','sks'],
        'data/tugas.csv': ['id_tugas','mata_kuliah','dosen_id','tugas','deskripsi','deadline','status'],
        'data/absensi.csv': ['nim','mata_kuliah','tanggal','status','keterangan']
    }
    for path, hdr in files.items():
        if not os.path.exists(path):
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(hdr)

def baca_csv(path):
    try:
        with open(path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []

def tulis_csv(path, rows, fieldnames):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def append_csv_row(path, row, fieldnames):
    exists = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)

# USER helpers
def find_user(username, password):
    users = baca_csv('data/users.csv')
    for u in users:
        if u['username'] == username and u['password'] == password:
            return u
    return None

def user_exists(username):
    users = baca_csv('data/users.csv')
    for u in users:
        if u['username'] == username:
            return True
    return False

def append_user(user_dict):
    append_csv_row('data/users.csv', user_dict, ['username','password','role','identitas'])

# small util to get dosen by id or username link
def get_dosen_by_user(username):
    # user.identitas for dosen stored as id_dosen
    users = baca_csv('data/users.csv')
    for u in users:
        if u['username'] == username and u['role']=='dosen':
            return u.get('identitas','')
    return ''

def export_txt(filename, content):
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Exported: {filename}")
