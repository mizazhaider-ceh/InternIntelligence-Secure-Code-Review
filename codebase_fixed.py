"""
Secure version of codebase.py, written as the follow-up to the Secure Code Review task.

Fixes applied (see FINDINGS.md for the full findings list):
1. No hardcoded credentials: the admin account is created from an ADMIN_PASSWORD
   environment variable, or from a first-run prompt when the variable is not set.
2. Parameterized SQL queries everywhere (no string formatting in queries).
3. Passwords stored as salted hashes (hashlib.pbkdf2_hmac, SHA-256, 210k iterations).
4. File uploads are sanitized: os.path.basename strips directory components,
   extensions are restricted to an allowlist, and the final path is checked
   to stay inside the uploads directory.
5. All user input is validated before use.

Educational demo only. Run it locally with: python3 codebase_fixed.py
"""

import hashlib
import os
import secrets
import sqlite3
from getpass import getpass

DB_NAME = "users_secure.db"
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf", ".png", ".jpg", ".jpeg", ".gif"}
PBKDF2_ITERATIONS = 210_000


def hash_password(password):
    """Hash a password with a random salt using PBKDF2-HMAC-SHA256."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return salt.hex() + ":" + digest.hex()


def verify_password(password, stored):
    """Verify a password against a stored salt:hash value."""
    try:
        salt_hex, digest_hex = stored.split(":")
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return secrets.compare_digest(digest.hex(), digest_hex)


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL)"
    )
    cursor.execute("SELECT 1 FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        admin_password = os.environ.get("ADMIN_PASSWORD")
        if not admin_password:
            print("First run: set the admin password.")
            while True:
                first = getpass("New admin password: ")
                second = getpass("Confirm admin password: ")
                if first == second and len(first) >= 8:
                    admin_password = first
                    break
                print("Passwords do not match or are shorter than 8 characters.")
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", hash_password(admin_password)),
        )
        conn.commit()
        print("Admin account created with a salted password hash.")
    conn.close()


def login():
    print("=== Login Page ===")
    username = input("Enter username: ").strip()
    password = getpass("Enter password: ")
    if not username or not password:
        print("Invalid credentials.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and verify_password(password, row[0]):
        print(f"Welcome, {username}!")
    else:
        print("Invalid credentials.")


def safe_upload_path(filename):
    """Return a safe absolute path for an uploaded file, or None if rejected."""
    name = os.path.basename(filename).strip()
    if not name or name in {".", ".."}:
        return None
    _, ext = os.path.splitext(name)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return None
    target = os.path.abspath(os.path.join(UPLOAD_DIR, name))
    if not target.startswith(os.path.abspath(UPLOAD_DIR) + os.sep):
        return None
    return target


def upload_file():
    print("\n=== File Upload ===")
    source = input("Enter the file name to upload: ").strip()
    if not os.path.isfile(source):
        print("File not found.")
        return

    target = safe_upload_path(source)
    if target is None:
        print("Upload rejected: filename is unsafe or the file type is not allowed.")
        return

    with open(source, "rb") as f:
        content = f.read()
    with open(target, "wb") as f:
        f.write(content)
    print(f"File uploaded to {target}")


def main():
    while True:
        print("\n1. Login\n2. Upload File\n3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            login()
        elif choice == "2":
            upload_file()
        elif choice == "3":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    init_db()
    main()
