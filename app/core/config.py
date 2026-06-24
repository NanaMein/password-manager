from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv(
    dotenv_path=(
        Path(__file__).resolve().parent.parent.parent
        / ".digital_locket_settings"
    )
)


class Settings:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent

        self._separator = os.getenv("separator")

        self._working_dir_name = os.getenv("working_directory_name")

        self._secret_vault_storage_name = os.getenv("secret_vault_storage_name")

        self._master_vault_file_name = os.getenv("master_vault_file_name")

        self._validation_vault_file_name = os.getenv("validation_vault_file_name")


    @property
    def separator(self):
        if not self._separator:
            return bytes("---80f8a4b0-0b4b-4623-ba12-0a711208f7b0---", "utf-8")
        return bytes(self._separator, "utf-8")

    @property
    def working_dir(self):
        if not self._working_dir_name:
            return self.base_path / "default_working_storage"
        return self.base_path / self._working_dir_name

    @property
    def secret_vault_storage(self):
        if not self._secret_vault_storage_name:
            return self.base_path / "default_secret_storage"
        return self.base_path / self._secret_vault_storage_name

    @property
    def master_vault_file(self):
        if not self._master_vault_file_name:
            return self.secret_vault_storage / "default-master.vault"
        return self.secret_vault_storage / self._master_vault_file_name

    @property
    def validation_vault_file(self):
        if not self._validation_vault_file_name:
            return self.secret_vault_storage / "default-validation.vault"
        return self.secret_vault_storage / self._validation_vault_file_name


def get_settings_instance():
    if not hasattr(get_settings_instance, "configurations"):
        get_settings_instance.configurations = Settings()
    return get_settings_instance.configurations
