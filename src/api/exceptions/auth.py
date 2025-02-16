from fastapi import HTTPException, status


class WrongUsernameOrPasswordError(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_401_UNAUTHORIZED,
                 detail: str = "Wrong username or password."):
        super().__init__(status_code, detail)


class RegisterNewUsernameConflictError(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_401_UNAUTHORIZED,
                 detail: str = "User with this username is already registered."):
        super().__init__(status_code, detail)


class NotLoggedInError(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_401_UNAUTHORIZED,
                 detail: str = "You are not logged in."):
        super().__init__(status_code, detail)
