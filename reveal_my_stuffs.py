from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pathlib import Path
import base64
import os

load_dotenv()
SEPARATOR = b"---80f8a4b0-0b4b-4623-ba12-0a711208f7b0---"
VAULT_PASSPHRASE = os.getenv("VAULT_PASSPHRASE", "").encode()

VAULT_FILE = Path("the_vault/master.vault")
OUTPUT_DIR = Path("unlock_secrets")



def derive_key(passphrase: bytes, salt: bytes) -> bytes:
    raw = hash_secret_raw(
        secret=passphrase,
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID
    )
    return base64.urlsafe_b64encode(raw)

def unlock_it():
    if not VAULT_PASSPHRASE:
        raise ValueError("VAULT_PASSPHRASE not provided")

    data = VAULT_FILE.read_bytes()
    salt, encrypted = data[:16], data[16:]

    key = derive_key(VAULT_PASSPHRASE, salt)

    _fernet = Fernet(key)

    decrypted = _fernet.decrypt(encrypted)

    parts = decrypted.split(SEPARATOR)
    count = 0
    for i in range(1, len(parts), 2):
        name = parts[i].decode()
        content = parts[i + 1]

        file_path = OUTPUT_DIR / name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)
        count += 1
    print(f"🔓 Restored {count} files → {OUTPUT_DIR}/")


if __name__ == "__main__":
    unlock_it()