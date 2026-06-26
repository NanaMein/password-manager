from cryptography.fernet import Fernet
from app.core.config import get_settings_instance
from app.services.key_derivation_service import KeyDerivationService






class ValidFileService:
    def __init__(self, derive_service: KeyDerivationService):
        self.derive_service = derive_service
        self.settings = get_settings_instance()

    def create_canary_vault(self, passphrase: str | bytes, salt: bytes):
        try:
            key = self.derive_service.get_key(passphrase=passphrase, salt=salt)
            token = Fernet(key).encrypt(self.settings.canary_vault_token)
            self.settings.canary_vault_file.write_bytes(salt + token)
            return True
        except Exception as e:
            return False

    def check_canary_vault(self, passphrase: str | bytes) -> bool:
        salt, token = self.derive_service.get_salt_and_token(self.settings.canary_vault_file)
        key = self.derive_service.get_key(passphrase=passphrase, salt=salt)
        try:
            decrypted = Fernet(key).decrypt(token)
            return decrypted == b"CANARY_VALID"
        except Exception as e:
            return False






