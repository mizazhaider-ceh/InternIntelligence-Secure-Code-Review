# Secure Code Review - Findings Summary

This is a short summary of the findings from my full report (`Secure-Code-Review.pdf`).
The reviewed script is `codebase.py`, a small Python app with a login system and a file upload feature.

> **Note:** `codebase.py` is intentionally vulnerable. It was written as the target of this review exercise. Do not use it as a starting point for a real application. See `codebase_fixed.py` for the same app with the fixes applied.

## Findings

| # | Finding | Severity | Where |
|---|---------|----------|-------|
| 1 | Hardcoded credentials (`admin` / `admin123`) written into the database at startup | High | `codebase.py`, module level |
| 2 | SQL injection in the login query (string-formatted query) | High | `login()` |
| 3 | Unrestricted file upload (no type or extension checks) | High | `upload_file()` |
| 4 | No input validation or sanitization; path traversal possible via the filename (`../../etc/passwd` style input) | High | `login()`, `upload_file()` |
| 5 | Passwords stored in plaintext in SQLite | High | database setup |

## Recommendations (applied in `codebase_fixed.py`)

- Use **parameterized queries** instead of string formatting for all SQL.
- Never hardcode credentials. Load secrets from environment variables or a secrets manager.
- Hash passwords with a salted, slow hash (the fixed version uses `hashlib.pbkdf2_hmac` from the standard library; `bcrypt`/`argon2` are the usual picks in production).
- Validate and sanitize filenames: strip directory components with `os.path.basename`, restrict extensions, and reject anything that escapes the upload directory.
- Validate all user input before use.

## How to run

```bash
# Vulnerable version (for the review exercise, local use only)
python3 codebase.py

# Fixed version
python3 codebase_fixed.py
```

Both scripts use only the Python standard library, so no dependencies to install.
The fixed version prompts for an admin password on first run and stores it as a salted hash.
