from fastapi import APIRouter, Cookie, Depends, HTTPException, Response

from api.schemas.auth import UserCredentialsSchema, UserSchema
from core.config import settings
from services.auth_service import AuthService

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register")
async def register(
    response: Response,
    user_creds: UserCredentialsSchema,
    auth_service: AuthService = Depends(AuthService),
) -> None:
    access_token = await auth_service.register(user_creds)
    if access_token is None:
        raise HTTPException(status_code=400, detail="Username is already taken.")

    response.set_cookie(
        key=settings.COOKIE_NAME, value=access_token, **settings.COOKIE_PARAMS
    )


@auth_router.post("/login")
async def login(
    response: Response,
    user_creds: UserCredentialsSchema,
    auth_service: AuthService = Depends(AuthService),
) -> None:
    access_token = await auth_service.login(user_creds)
    if access_token is None:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    response.set_cookie(
        key=settings.COOKIE_NAME, value=access_token, **settings.COOKIE_PARAMS
    )


@auth_router.get("/current_user")
async def get_current_user(
    auth_service: AuthService = Depends(AuthService),
    access_token: str | None = Cookie(alias=settings.COOKIE_NAME, default=None),
) -> UserSchema:
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not logged in.")

    user = await auth_service.get_user(access_token)
    if user is None:
        raise HTTPException(status_code=401, detail="Not logged in.")

    return UserSchema.model_validate(user)


@auth_router.post("/logout")
async def logout(response: Response) -> None:
    response.delete_cookie(settings.COOKIE_NAME)
