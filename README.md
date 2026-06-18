# 🔐 USB Password Manager (Plug & Play)

A portable, self-contained password manager that runs entirely from a USB drive. Just plug it in, and access your secure vault via a local web interface—no installation or technical setup required!

## ✨ Features
- **True Plug & Play**: Bundled Python environment (`.venv`) + FastAPI server auto-starts on USB insertion.
- **Local Web UI**: Manage passwords at `http://localhost:8888` (non-technical friendly).
- **Military-Grade Security**:
  - 🔑 **Argon2-cffi**: Hashes master tokens with memory-hard resistance.
  - 🔒 **Fernet Encryption**: Encrypts/decrypts files & credentials (AES-128-CBC + HMAC).
- **Zero Cloud Dependency**: All data stays on your USB. Air-gapped by design.
- **Portable**: Works on Windows/macOS/Linux with bundled dependencies.

## 🚀 Quick Start
1. Insert USB → Server auto-launches (or run `start.bat`/`start.sh` manually).
2. Open browser → `http://localhost:8888`.
3. Set master token → Store/retrieve passwords securely.

## 🔧 Tech Stack
- **Backend**: FastAPI + Uvicorn
- **Crypto**: `argon2-cffi` + `cryptography` (Fernet)
- **Frontend**: Vanilla HTML/CSS/JS (lightweight)
- **Runtime**: Embedded Python `.venv` on USB

## ⚠️ Security Notes
- Master token is **never stored**—only its Argon2 hash.
- Fernet keys derived from token via PBKDF2 (salted).
- USB loss = data loss. **Back up encrypted vault!**
- For advanced users: Audit code in `/src/crypto.py`.

## 🛣️ Roadmap
- [ ] Auto-detect USB mount & launch server
- [ ] Biometric unlock (WebAuthn)
- [ ] Encrypted backup/export
- [ ] Cross-platform USB autorun scripts

## 💡 Why This?
Built for non-tech users who want **physical control** over their secrets. No cloud, no accounts, no complexity. Just plug in and trust your hardware.

---
*Disclaimer: This is a personal project. Use at your own risk. Always verify crypto implementations for production.*
