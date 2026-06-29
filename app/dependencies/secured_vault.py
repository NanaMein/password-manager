from app.services.key_derivation_service import KeyDerivationService
from app.services.validation_service import ValidFileService
from app.services.locking_service import LockFileService
from app.services.unlocking_service import UnlockingFileService
from app.services.orchestrator_service import OrchestratorService
from fastapi import Depends, Request



def get_key_derivation_service() -> KeyDerivationService:
    return KeyDerivationService()

def get_lock_file_service(derive_service = Depends(get_key_derivation_service)) -> LockFileService:
    return LockFileService(key_derivation_service=derive_service)

def get_unlock_file_service(derive_service = Depends(get_key_derivation_service)) -> UnlockingFileService:
    return UnlockingFileService(key_derivation_service=derive_service)

def get_validation_service(derive_service = Depends(get_key_derivation_service)) -> ValidFileService:
    return ValidFileService(derive_service=derive_service)

def get_orchestrator_service(
        request: Request,
        lock_service = Depends(get_lock_file_service),
        unlock_service = Depends(get_unlock_file_service),
        validation_service = Depends(get_validation_service),
        derive_service = Depends(get_key_derivation_service),
) -> OrchestratorService:
    return OrchestratorService(
        key_derivation_service=derive_service,
        locking_service=lock_service,
        unlocking_service=unlock_service,
        validation_service=validation_service,
        request=request
    )