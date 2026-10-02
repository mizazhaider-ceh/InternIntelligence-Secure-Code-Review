"""
INTENTIONALLY VULNERABLE - educational secure code review target.

This script was written on purpose as a vulnerable codebase to review and
report on for an internship task (see FINDINGS.md and Secure-Code-Review.pdf).
It contains real vulnerabilities: hardcoded credentials, SQL injection,
unrestricted file upload, path traversal, and plaintext password storage.

Do NOT copy this code into a real application. For the secured version of
the same app, see codebase_fixed.py.
"""

import os
import sqlite3


conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")  # Hardcoded user
conn.commit()

def login():
    print("=== Login Page ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        print(f"Welcome, {username}!")
    else:
        print("Invalid credentials.")

def upload_file():
    print("\n=== File Upload ===")
    filename = input("Enter the file name to upload: ")
    

    with open(filename, 'rb') as f:
        content = f.read()

    upload_path = f"uploads/{filename}" 
    with open(upload_path, 'wb') as f:
        f.write(content)
    print(f"File uploaded to {upload_path}")

def main():
    while True:
        print("\n1. Login\n2. Upload File\n3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            login()
        elif choice == '2':
            upload_file()
        elif choice == '3':
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.mkdir("uploads")
    main()
