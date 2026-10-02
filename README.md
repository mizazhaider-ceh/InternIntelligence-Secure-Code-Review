# 🛡️ Secure Code Review - Python Application

## 📌 Overview

I reviewed a deliberately vulnerable Python app (a simple login system plus a file upload feature) for common security issues, documented every finding, and wrote the report as a formal task deliverable.

- `codebase.py` — the intentionally vulnerable codebase that was reviewed
- `codebase_fixed.py` — the same app rewritten with the fixes applied (parameterized queries, salted password hashes, sanitized uploads, no hardcoded credentials)
- `FINDINGS.md` — short summary of the findings and recommendations
- `Secure-Code-Review.pdf` — the full task report with analysis, findings, and recommendations

> ⚠️ **Educational use only.** `codebase.py` is vulnerable on purpose. Do not use it as a base for real software.

## 🎯 What I did

- Reviewed the code for common flaws: SQL injection, hardcoded credentials, insecure file handling, missing input validation, plaintext password storage
- Documented each finding with the exact vulnerable code and the risk it creates
- Wrote practical remediation recommendations, then implemented them in `codebase_fixed.py`
- Delivered the full process as a formal security report (`Secure-Code-Review.pdf`)

## 🗂️ Files

| File | Purpose |
|------|---------|
| `codebase.py` | Vulnerable review target (educational, local use only) |
| `codebase_fixed.py` | Secured version implementing the recommendations |
| `FINDINGS.md` | Findings and recommendations summary |
| `Secure-Code-Review.pdf` | Complete lab report with analysis, findings, and recommendations |

## ▶️ Running the code

Both scripts use only the Python standard library. No install needed.

```bash
# Vulnerable version (for the review exercise, local use only)
python3 codebase.py

# Fixed version (creates users_secure.db and an uploads/ folder)
python3 codebase_fixed.py
```

The fixed version asks you to set an admin password on first run (or reads it from the `ADMIN_PASSWORD` environment variable) and stores it as a salted PBKDF2 hash.

## 🔎 Key findings (short version)

1. **Hardcoded credentials** — `admin` / `admin123` written into the database at startup
2. **SQL injection** — login query built with string formatting
3. **Unrestricted file upload** — no file type checks
4. **No input validation** — path traversal possible via the filename
5. **Plaintext password storage** — credentials readable by anyone with DB access

## 👤 Task info

**Muhammad Izaz Haider** — Penetration Tester
Assigned by **Intern Intelligence** · Completed **7 April 2025**

🔗 [LinkedIn](https://www.linkedin.com/in/muhammad-izaz-haider-091639314/)
