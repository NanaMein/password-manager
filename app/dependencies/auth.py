from fastapi import Depends, Request, Response
from app.services.auth_service import AccessTokenService, RefreshTokenService




def get_access_token_service(
        request: Request,
        response: Response,
):
    return AccessTokenService(request, response)

def get_refresh_token_service(
        request: Request,
        response: Response,
):
    return RefreshTokenService(request, response)


def get_user_pass_phrase(
        access_token_service: AccessTokenService = Depends(get_access_token_service),
        refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service)
) -> str | None:
    _access_token, _access_id = access_token_service.get_token_and_id()
    if _access_token:
        return _access_id

    _refresh_token, _refresh_id = refresh_token_service.get_token_and_id()
    if _refresh_token:
        refresh_token_service.reset_cache(_refresh_token)

        access_token_service.create_token(_refresh_id)

        refresh_token_service.create_token(_refresh_id)
        return _refresh_id

    return None
