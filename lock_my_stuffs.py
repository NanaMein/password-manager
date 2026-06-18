from pathlib import Path
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
from argon2.low_level import hash_secret_raw, Type
import base64
import os

load_dotenv()

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

    combined = b""
    files = list(INPUT_DIR.rglob("*"))
    for f in files:
        if f.is_file():
            content = f.read_bytes()
            rel_path = f.relative_to(INPUT_DIR).as_posix()
            combined += f"<<<{rel_path}>>>".encode() + content

    encrypted = fernet.encrypt(combined)
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_bytes(salt + encrypted)

    file_count = len([f for f in files if f.is_file()])
    print(f"🔒 Encrypted {file_count} files → {OUTPUT_FILE}")

if __name__ == "__main__":
    lock_it()