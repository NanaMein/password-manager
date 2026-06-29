from app.core.config import get_settings_instance
from app.services.key_derivation_service import KeyDerivationService
from cryptography.fernet import Fernet
import io
import os



class LockFileService:
    def __init__(self, key_derivation_service: KeyDerivationService):
        self.settings = get_settings_instance()
        self.derive_key = key_derivation_service

    @staticmethod
    def get_salt():
        return os.urandom(16)

    def lock_files(self, passphrase: bytes | str, salt: bytes):
        if isinstance(passphrase, str):
            passphrase = bytes(passphrase, "utf-8")

        key = self.derive_key.get_key(passphrase=passphrase, salt=salt)


        files_status = {}
        try:
            buffer = io.BytesIO()
            files = [
                f for f in self.settings.working_dir.rglob("*") if f.is_file()
            ]
            for f in files:
                rel_path = f.relative_to(self.settings.working_dir).as_posix().encode()
                buffer.write(self.settings.separator)
                buffer.write(rel_path)
                buffer.write(self.settings.separator)
                buffer.write(f.read_bytes())

            encrypted = Fernet(key).encrypt(buffer.getvalue())
            self.settings.master_vault_file.write_bytes(salt + encrypted)
            files_status["status"] = "Ok"
            files_status["files_locked"] = len(files)
            return files_status

        except Exception as e:
            files_status["status"] = "Error"
            files_status["details"] = str(e)

    def lock_files_v1(self, passphrase: bytes | str):
        if isinstance(passphrase, str):
            passphrase = bytes(passphrase, "utf-8")

        key, salt = self.derive_key.get_key_and_salt(passphrase=passphrase)


        files_status = {}
        try:
            buffer = io.BytesIO()
            files = [
                f for f in self.settings.working_dir.rglob("*") if f.is_file()
            ]
            for f in files:
                rel_path = f.relative_to(self.settings.working_dir).as_posix().encode()
                buffer.write(self.settings.separator)
                buffer.write(rel_path)
                buffer.write(self.settings.separator)
                buffer.write(f.read_bytes())

            encrypted = Fernet(key).encrypt(buffer.getvalue())
            self.settings.master_vault_file.write_bytes(salt + encrypted)
            files_status["status"] = "Ok"
            files_status["files_locked"] = len(files)
            return files_status

        except Exception as e:
            files_status["status"] = "Error"
            files_status["details"] = str(e)
            return files_status
