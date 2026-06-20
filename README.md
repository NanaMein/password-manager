***

# 🔐 Di-Lock (Digital Locket)
### *Your Personal Sanctuary on a USB*

**Di-Lock** is a "Digital Locket" for your most important treasures. Unlike a regular folder, Di-Lock keeps your passwords, private photos, sensitive documents, and videos behind a high-security vault that lives entirely on your USB drive. 

No cloud, no accounts, no footprints. Just plug it in, unlock your locket, and keep your secrets safe.

---

## 🌟 Why Di-Lock? (For Non-Techies)
Most security tools are complicated. Di-Lock is built to be **Plug & Play**:
*   **Physical Security**: If you don't have the USB, the data doesn't exist.
*   **Total Privacy**: Your files never touch the internet. They stay on your hardware.
*   **Amnesia Feature**: The "key" to your vault is only kept in the computer's temporary memory (RAM). The moment you unplug the USB or close the app, the key evaporates. Even if someone steals your laptop later, they won't find the key!
*   **Self-Cleaning**: Every time you start Di-Lock, it automatically sweeps away any leftover traces of decrypted files, making sure your business stays your business.

## 🚀 How to Use
1.  **Plug in your USB** to a Windows computer.
2.  **Run `start.bat`** (the Locket's "Power" button).
3.  **Open your browser** to `http://localhost:54321`.
4.  **Enter your Passphrase**: 
    *   *First time?* Create a strong passphrase (12-40 characters). This is the *only* key to your locket.
    *   *Returning?* Enter your passphrase to see your treasures.

## 🛡️ How it Protects You (Transparency)
We believe you should know exactly how your Locket works:
*   **The Vault (Argon2 & Fernet)**: We use industry-standard "Military Grade" encryption to scramble your files. They cannot be read without your specific passphrase.
*   **The RAM Lock (TTL Cache)**: We **never** save your passphrase on the USB or the computer. It is stored in a temporary "cache" that automatically deletes itself after 30 minutes of inactivity.
*   **The Secure Sweep**: When the program starts, it scans for any files you might have forgotten to re-encrypt and securely overwrites them so they can't be recovered by specialists.
*   **Safety First**: If a vault already exists on the USB, Di-Lock won't let a new user overwrite it. Your memories are protected from accidental overwrite.

## ⚙️ Tech Specs (For the Curious)
- **Engine**: FastAPI (Python-based)
- **Encryption**: Fernet (AES-128-CBC)
- **Hashing**: Argon2-cffi
- **Platform**: Optimized for **Windows**.
- **License**: Apache 2.0 (Open Source & Transparent)

---
## ⚠️ A Personal Note & Disclaimer
**Di-Lock** is an open-source project shared under the **Apache 2.0 License**. 

*   **Master's Choice**: This is the exact tool the creator uses to protect his own personal documents, photos, and secrets. It is built with a "security-first" mindset.
*   **Hardware Responsibility**: As this is software, the creator cannot be held responsible for hardware-related issues. If your USB drive is physically damaged, the files are corrupted by the OS, or you accidentally reformat the drive, your data will be lost.
*   **The Golden Rule**: There is no "Forgot Password" button. If you lose your passphrase, the encryption cannot be reversed. 
*   **Plug at Your Own Risk**: While this tool is designed for privacy and safety, please ensure you maintain your own encrypted backups. You are responsible for the hardware you choose to use.

---
*“I guard my own secrets with my life, but even I cannot fix a broken USB! Please be careful with your treasures.” — Nana Mein*

***
