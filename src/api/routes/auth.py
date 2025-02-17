from fastapi import APIRouter, Cookie, Depends, Response, Request

from api.schemas.auth import UserCredentialsSchema, UserSchema
from core.config import settings
from api.exceptions.auth import RegisterNewUsernameConflictError, WrongUsernameOrPasswordError, NotLoggedInError
from services.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])

async def get_current_user(
        auth_service: AuthService = Depends(AuthService),
        access_token: str | None = Cookie(alias=settings.COOKIE_NAME, default=None),
) -> UserSchema:
    if access_token is None:
        raise NotLoggedInError()

    user = await auth_service.get_user(access_token)
    if user is None:
        raise NotLoggedInError()

    return UserSchema.model_validate(user, from_attributes=True)


@auth_router.post("/register")
async def register(
        response: Response,
        user_creds: UserCredentialsSchema,
        auth_service: AuthService = Depends(AuthService),
) -> None:
    access_token = await auth_service.register(user_creds)
    if access_token is None:
        raise RegisterNewUsernameConflictError()

    response.set_cookie(
        key=settings.COOKIE_NAME, value=access_token, expires=settings.COOKIE_AGE,
    )


@auth_router.post("/login")
async def login(
        response: Response,
        user_creds: UserCredentialsSchema,
        auth_service: AuthService = Depends(AuthService),
) -> None:
    access_token = await auth_service.login(user_creds)
    if access_token is None:
        raise WrongUsernameOrPasswordError()

    response.set_cookie(
        key=settings.COOKIE_NAME, value=access_token, expires=settings.COOKIE_AGE,
    )


@auth_router.get("/current_user")
async def current_user(
        current_user: UserSchema = Depends(get_current_user)
) -> UserSchema:
    return current_user


@auth_router.post("/logout")
async def logout(response: Response) -> None:
    response.delete_cookie(settings.COOKIE_NAME)
