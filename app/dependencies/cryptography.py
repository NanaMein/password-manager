from app.services.cryptography_service import DeriveKeyService, LockFileService, EncryptFileService
from fastapi import Depends



def get_derive_key_service():
    return DeriveKeyService()

def get_lock_file_service(
    derive_key_service: DeriveKeyService = Depends(get_derive_key_service)
):
    return LockFileService(
        derive_key_service=derive_key_service
    )

def get_encrypt_file_service(
        derive_key_service: DeriveKeyService = Depends(get_derive_key_service)
):
    return EncryptFileService(
        derive_key_service=derive_key_service
    )