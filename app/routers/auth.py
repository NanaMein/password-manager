from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.auth_service import AccessTokenService, RefreshTokenService
from app.dependencies.auth import get_refresh_token_service, get_access_token_service, get_user_pass_phrase



router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

class Form(BaseModel):
    passphrase: str


@router.post("/init-session")
def initialize_session(
        user_form: Form,
        user_id: str = Depends(get_user_pass_phrase),
        acc_tkn_serv: AccessTokenService = Depends(get_access_token_service),
        rfs_tkn_serv: RefreshTokenService = Depends(get_refresh_token_service)
):
    if user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    if rfs_tkn_serv.get_token():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    try:
        acc_tkn_serv.create_token(subject=user_form.passphrase)
        rfs_tkn_serv.create_token(subject=user_form.passphrase)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@router.get("/me")
def get_me(
        user_id: str=Depends(get_user_pass_phrase),
):
    if user_id:
        return {"user_id": user_id}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)







