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
VALIDATION_FILE = VAULT_DIR / "validation.vault"

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

def _create_canary(passphrase: bytes, salt: bytes):
    key = derive_key(passphrase, salt)
    fernet = Fernet(key)

    canary_token = fernet.encrypt(b"CANARY_VALID")
    VALIDATION_FILE.write_bytes(salt + canary_token)


def lock_it():
    if not VAULT_PASSPHRASE:
        raise ValueError("VAULT_PASSPHRASE not found in .env file.")

    try:
        VAULT_DIR.mkdir(parents=True, exist_ok=True)
        test_file = VAULT_DIR / ".write_test"
        test_file.touch()
        test_file.unlink()
    except PermissionError as e:
        raise PermissionError(
            f"\n❌ WRITE ACCESS DENIED!\n"
            f"   Cannot write to {VAULT_DIR}\n"
            f"   Check folder permissions before proceeding."
        ) from e

    valid_file_exists = VALIDATION_FILE.exists()
    output_file_exists = OUTPUT_FILE.exists()

    if valid_file_exists != output_file_exists:
        raise RuntimeError(
            f"\n⚠️ VAULT CORRUPTED!\n"
            f"   Found {'only canary' if valid_file_exists else 'only master vault'}.\n"
            f"   Both files must exist together. Manual cleanup required."
        )

    if valid_file_exists:
        existing_file = VALIDATION_FILE.read_bytes()
        test_salt = existing_file[:16]
        test_encrypted = existing_file[16:]

        try:
            test_key = derive_key(VAULT_PASSPHRASE, test_salt)
            test_fernet = Fernet(test_key)
            test_fernet.decrypt(test_encrypted)


            print("✅ Passphrase verified. Safe to overwrite.")
        except InvalidToken:
            raise PermissionError("❌ Wrong passphrase! Vault locked.")
        except Exception:
            raise PermissionError("❌ Wrong passphrase or corrupted canary! Vault locked.")

    if not INPUT_DIR.exists() or not any(INPUT_DIR.rglob("*")):
        raise ValueError(f"❌ Input directory '{INPUT_DIR}' is missing or empty!")

    salt = os.urandom(16)
    key = derive_key(VAULT_PASSPHRASE, salt)
    fernet = Fernet(key)

    _create_canary(passphrase=VAULT_PASSPHRASE, salt=salt)

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
    OUTPUT_FILE.write_bytes(salt + encrypted)
    print(f"🔒 Encrypted {len(files)} files → {OUTPUT_FILE}")

if __name__ == "__main__":
    lock_it()