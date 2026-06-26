import os
from pathlib import Path
from argon2.low_level import hash_secret_raw, Type
from base64 import urlsafe_b64encode




class KeyDerivationService:

    @staticmethod
    def _derive_key(passphrase, salt):
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

    def get_key(self, passphrase: str | bytes, salt: bytes):

        if isinstance(passphrase, str):
            passphrase = bytes(passphrase, 'utf-8')

        return self._derive_key(passphrase, salt)

    def get_key_and_salt(self, passphrase: str | bytes):
        if isinstance(passphrase, str):
            passphrase = bytes(passphrase, 'utf-8')

        salt = os.urandom(16)
        key = self._derive_key(passphrase, salt)
        return key, salt


    def get_salt_and_token(self, file: Path | bytes):
        if isinstance(file, Path):
            file = file.read_bytes()
        salt_length = 16
        salt =file[:salt_length]
        token = file[salt_length:]
        return salt, token

