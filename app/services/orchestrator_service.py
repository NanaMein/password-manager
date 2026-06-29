from app.services.key_derivation_service import KeyDerivationService
from app.services.unlocking_service import UnlockingFileService
from app.services.locking_service import LockFileService
from app.services.validation_service import ValidFileService
from app.core.lifespan import StartupStatus
from core.config import get_settings_instance
from app.core.state import app_state
from fastapi import Request



class OrchestratorService:
    def __init__(
            self,
            key_derivation_service: KeyDerivationService,
            unlocking_service: UnlockingFileService,
            locking_service: LockFileService,
            validation_service: ValidFileService,
            request: Request
    ):
        self.settings = get_settings_instance()
        self.derive_key = key_derivation_service
        self.unlock = unlocking_service
        self.lock = locking_service
        self.validation = validation_service
        self.request = request

    @property
    def startup_status(self) -> StartupStatus:
        return self.request.app.state.startup_status

    def check_passphrase_validity(self, passphrase: str) -> bool:
        if not self.validation.check_canary_vault(passphrase):
            if not self.unlock.check_vault_validity(passphrase):
                return False
        return True

    def save_my_files(self, passphrase):
        salt = self.lock.get_salt()

        user_status = app_state.user_status

        if user_status == "NEW_USER":
            self.lock.lock_files(passphrase=passphrase, salt=salt)
            self.validation.create_canary_vault(passphrase=passphrase, salt=salt)
            app_state.user_status = "EXISTING_USER"
        elif user_status == "EXISTING_USER":
            self.lock.lock_files(passphrase=passphrase, salt=salt)
            self.validation.create_canary_vault(passphrase=passphrase, salt=salt)
        else:
            raise ValueError("User status must be NEW_USER or EXISTING_USER")
        return True

    def unlock_my_files(self, passphrase):
        if not self.check_passphrase_validity(passphrase):
            return False
        return self.unlock.unlock_files(passphrase=passphrase)
