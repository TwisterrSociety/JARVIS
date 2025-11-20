from modules.utils import (
    typing, pause, ensure_data_files, find_user,
    user_exists, append_user, rand_password
)
from modules.mahasiswa import menu_mahasiswa
from modules.dosen import menu_dosen
from modules.admin import menu_admin

# ============================================================
# STARTUP
# ============================================================

def welcome_screen():
    print("============================================================")
    print("                🧠 SINTAK OS v3.2 SYSTEM                    ")
    print("============================================================")
    print("1. Login")
    print("2. Register (buat akun baru) — hanya Mahasiswa")
    print("3. Keluar")
    print("============================================================")

    return input("Pilih menu: ").strip()


# ============================================================
# REGISTER SYSTEM (Mahasiswa only)
# ============================================================

def register_account():
    typing("\n🔐 MEMBUAT AKUN BARU (MAHASISWA)...\n", 0.01)

    while True:
        username = input("Username baru (NIM): ").strip()
        if user_exists(username):
            typing("❌ Username sudah dipakai, coba lagi.", 0.01)
        else:
            break

    password = input("Password (kosong = generate otomatis): ").strip()
    if not password:
        password = rand_password()
        typing(f"🔑 Password otomatis: {password}", 0.01)

    # role otomatis mahasiswa; identitas = NIM
    role = "mahasiswa"
    ident = username

    new_user = {
        "username": username,
        "password": password,
        "role": role,
        "identitas": ident
    }

    append_user(new_user)
    typing("\n✅ Akun mahasiswa berhasil dibuat! Simpan password dengan aman.", 0.01)
    pause()


# ============================================================
# LOGIN SYSTEM
# ============================================================

def login_panel():
    print("============================================================")
    print("          🔐 SINTAK OS LOGIN PANEL")
    print("============================================================")
    username = input("Username : ").strip()
    password = input("Password : ").strip()

    user = find_user(username, password)
    if not user:
        typing("❌ Login gagal! Username atau password salah.", 0.01)
        pause()
        return None

    typing(f"\n✅ Login berhasil. Selamat datang, {username}!", 0.01)
    return user


# ============================================================
# MAIN SYSTEM ROUTER
# ============================================================

def run_sintak():
    ensure_data_files()

    while True:
        choice = welcome_screen()

        if choice == '1':        # LOGIN
            user = login_panel()
            if user:
                if user["role"] == "mahasiswa":
                    menu_mahasiswa(user)
                elif user["role"] == "dosen":
                    menu_dosen(user)
                elif user["role"] == "admin":
                    menu_admin(user)

        elif choice == '2':      # REGISTER (Mahasiswa only)
            register_account()

        elif choice == '3':      # EXIT
            typing("\n👋 Keluar dari sistem...", 0.01)
            break

        else:
            typing("❌ Menu tidak valid!", 0.01)
            pause()


if __name__ == "__main__":
    run_sintak()
