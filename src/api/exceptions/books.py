from fastapi import HTTPException, status


class BookNotFoundError(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_404_NOT_FOUND,
                 detail: str = "Book not found."):
        super().__init__(status_code, detail)


class BookNameConflictError(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_409_CONFLICT,
                 detail: str = "Book with this title already exists."):
        super().__init__(status_code, detail)
