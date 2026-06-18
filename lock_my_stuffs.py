from pathlib import Path
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
from argon2.low_level import hash_secret_raw, Type
import base64
import os
import io

load_dotenv()

SEPARATOR = b"---80f8a4b0-0b4b-4623-ba12-0a711208f7b0---"
VAULT_PASSPHRASE = os.getenv("VAULT_PASSPHRASE", "").encode()
INPUT_DIR = Path("my_secrets")
VAULT_DIR = Path("the_vault")
OUTPUT_FILE = VAULT_DIR / "master.vault"

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

def lock_it():
    if not VAULT_PASSPHRASE:
        raise ValueError("VAULT_PASSPHRASE not found in .env file.")

    if OUTPUT_FILE.exists():
        existing_file = OUTPUT_FILE.read_bytes()
        salt = existing_file[:16]
        encrypted = existing_file[16:]

        test_key = derive_key(VAULT_PASSPHRASE, salt)
        test_fernet = Fernet(test_key)

        try:
            test_fernet.decrypt(encrypted)
            print("✅ Passphrase matches. Overwriting vault with new content...")
        except InvalidToken:
            raise PermissionError(
                f"\n❌ VAULT LOCKED!\n"
                f"   The existing {OUTPUT_FILE} was created with a DIFFERENT passphrase.\n"
                f"   To overwrite it, you must manually delete or rename the file first.\n"
                f"   (This protects you from accidentally losing your data.)"
            )

    salt = os.urandom(16)
    key = derive_key(VAULT_PASSPHRASE, salt)
    fernet = Fernet(key)

    buffer = io.BytesIO()
    files = [
        f for f in INPUT_DIR.rglob("*") if f.is_file()
    ]
    for f in files:
        rel_path = f.relative_to(INPUT_DIR).as_posix().encode()
        buffer.write(SEPARATOR)
        buffer.write(rel_path)
        buffer.write(SEPARATOR)
        buffer.write(f.read_bytes())

    encrypted = fernet.encrypt(buffer.getvalue())
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_bytes(salt + encrypted)
    print(f"🔒 Encrypted {len(files)} files → {OUTPUT_FILE}")

if __name__ == "__main__":
    lock_it()