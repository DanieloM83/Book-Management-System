from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
    ],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
