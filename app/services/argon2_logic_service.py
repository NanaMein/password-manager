from pathlib import Path
from argon2.low_level import hash_secret_raw, Type
from base64 import urlsafe_b64encode

class ArgonDeriveService:

    def get_key(self, passphrase: str | bytes, salt: bytes):

        if isinstance(passphrase, str):
            passphrase = bytes(passphrase, 'utf-8')

        return urlsafe_b64encode(
            hash_secret_raw(
                secret=passphrase,
                salt=salt,
                time_cost=3,
                memory_cost=65536,
                parallelism=4,
                hash_len=32,
                type=Type.ID
            )
        )

    def get_salt_and_token(self, file: Path):
        existing_file = file.read_bytes()
        salt_length = 16
        salt =existing_file[:salt_length]
        token = existing_file[salt_length:]
        return salt, token