from app.core.config import get_settings_instance
from app.services.key_derivation_service import KeyDerivationService
from cryptography.fernet import Fernet, InvalidToken


class UnlockingFileService:
    def __init__(self, key_derivation_service: KeyDerivationService):
        self.settings = get_settings_instance()
        self.derive_key = key_derivation_service

    def decrypted_fernet(self, passphrase: str | bytes):
        if isinstance(passphrase, str):
            passphrase = bytes(passphrase, "utf-8")
        try:
            salt, token = self.derive_key.get_salt_and_token(self.settings.master_vault_file)
            key = self.derive_key.get_key(passphrase, salt)
            decrypted = Fernet(key).decrypt(token)
            return decrypted
        except InvalidToken as iex:
            raise iex
        except Exception as ex:
            raise ex

    def check_vault_validity(self, passphrase: bytes | str):
        if isinstance(passphrase, str):
            passphrase = bytes(passphrase, "utf-8")

        try:
            self.decrypted_fernet(passphrase)
            return True
        except (InvalidToken, Exception) as iex:
            return False

    def unlock_files(self, passphrase: bytes | str):
        try:
            decrypted = self.decrypted_fernet(passphrase)
            parts = decrypted.split(self.settings.separator)
            count = 0
            for i in range(1, len(parts), 2):
                name = parts[i].decode()
                content = parts[i + 1]

                file_path = self.settings.working_dir / name
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_bytes(content)
                count += 1
            return True
        except (InvalidToken, Exception) as e:
            return False


    def unlock_files_old(self, passphrase: bytes | str):
        file_status = {}
        if isinstance(passphrase, str):
            passphrase = bytes(passphrase, "utf-8")
        try:
            salt, token = self.derive_key.get_salt_and_token(self.settings.master_vault_file)
            key = self.derive_key.get_key(passphrase, salt)
            decrypted = Fernet(key).decrypt(token)
            file_status["status"] = "Ok"
        except (InvalidToken, Exception) as iex:
            file_status["status"] = "Error"
            file_status["details"] = str(iex)

        try:
            parts = decrypted.split(self.settings.separator)
            count = 0

            for i in range(1, len(parts), 2):
                name = parts[i].decode()
                content = parts[i + 1]

                file_path = self.settings.working_dir / name
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_bytes(content)
                count += 1
            file_status["files_unlocked"] = count
            return file_status
        except Exception as e:
            return file_status

