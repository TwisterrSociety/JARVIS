import csv
import os

def ensure_data_files():
    """Pastikan semua file CSV yang dibutuhkan sudah ada."""
    os.makedirs("data", exist_ok=True)

    data_files = {
        "data/users.csv": ['username', 'password', 'role', 'identitas'],
        "data/mahasiswa.csv": ['nim', 'nama', 'kelas', 'jurusan'],
        "data/nilai.csv": ['nim', 'nama', 'nilai'],
        "data/kehadiran.csv": ['nim', 'nama', 'tanggal', 'status']
    }

    for path, headers in data_files.items():
        if not os.path.exists(path):
            with open(path, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()

def read_csv(filepath):
    """Membaca file CSV dan mengembalikan list of dict."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline='', encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(filepath, data, fieldnames):
    """Menimpa seluruh isi file CSV dengan data baru."""
    with open(filepath, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv_row(filepath, row, fieldnames):
    """Menambah 1 baris ke file CSV."""
    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def find_user(username, password):
    """Cari user berdasarkan username dan password."""
    users = read_csv("data/users.csv")
    for u in users:
        if u["username"] == username and u["password"] == password:
            return u
    return None

def user_exists(username):
    """Cek apakah username sudah terdaftar."""
    users = read_csv("data/users.csv")
    return any(u["username"] == username for u in users)

def append_user(user_dict):
    """Menambahkan user baru ke users.csv."""
    append_csv_row("data/users.csv", user_dict, ['username','password','role','identitas'])

def clear_screen():
    """Membersihkan layar terminal (Windows/Linux)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Pause sederhana untuk CLI."""
    input("\nTekan Enter untuk melanjutkan...")
