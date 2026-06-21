from pathlib import Path
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
from argon2.low_level import hash_secret_raw, Type
import base64
import os
import io

load_dotenv()

class DeriveKeyService:

    def get_key(self, passphrase: bytes, salt: bytes):
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

class LockFileService:
    separator = b"---80f8a4b0-0b4b-4623-ba12-0a711208f7b0---"
    input_dir = Path("my_secrets")
    vault_dir = Path("the_vault")
    output_file = vault_dir / "master.vault"

    def __init__(self, derive_key_service: DeriveKeyService):
        self._derive_key_service = derive_key_service

    def check_file_and_passphrase_exist(self, passphrase: bytes | str):
        if isinstance(passphrase, str):
            passphrase = passphrase.encode()
        if self.output_file.exists():
            existing_file = self.output_file.read_bytes()
            salt = existing_file[:16]
            encrypted = existing_file[16:]

            validation_key = self._derive_key_service.get_key(
                passphrase=passphrase,
                salt=salt
            )
            validation_fernet = Fernet(validation_key)
            try:
                validation_fernet.decrypt(encrypted)
            except InvalidToken:
                raise PermissionError(
                f"\n❌ VAULT LOCKED!\n"
                f"   The existing {self.output_file} was created with a DIFFERENT passphrase.\n"
                f"   To overwrite it, you must manually delete or rename the file first.\n"
                f"   (This protects you from accidentally losing your data.)"
            )

    def execute_lock_filed(self, passphrase: str, salt: bytes):
        vault_passphrase = passphrase.encode()

        # if self.output_file.exists():
        #     existing_file = self.output_file.read_bytes()
        #     salt = existing_file[:16]
        #     encrypted = existing_file[16:]
        #
        #     validation_key = self._derive_key_service.get_key(vault_passphrase, salt)
        #     validation_fernet = Fernet(validation_key)
        #     try:
        #         validation_fernet.decrypt(encrypted)
        #     except InvalidToken:
        #         raise PermissionError(
        #         f"\n❌ VAULT LOCKED!\n"
        #         f"   The existing {self.output_file} was created with a DIFFERENT passphrase.\n"
        #         f"   To overwrite it, you must manually delete or rename the file first.\n"
        #         f"   (This protects you from accidentally losing your data.)"
        #     )

        self.check_file_and_passphrase_exist(passphrase=vault_passphrase)

        salt = os.urandom(16)
        key = self._derive_key_service.get_key(vault_passphrase, salt)
        fernet = Fernet(key)

        buffer = io.BytesIO()
        files = [
            f for f in self.input_dir.rglob("*") if f.is_file()
        ]
        for f in files:
            rel_path = f.relative_to(self.input_dir).as_posix().encode()
            buffer.write(self.separator)
            buffer.write(rel_path)
            buffer.write(self.separator)
            buffer.write(f.read_bytes())

        encrypted = fernet.encrypt(buffer.getvalue())
        self.output_file.parent.mkdir(exist_ok=True)
        self.output_file.write_bytes(salt + encrypted)
        print(f"🔒 Encrypted {len(files)} files → {self.output_file}")

