from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from src.app.router import currency_router, account_router

from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate, UserUpdate


app = FastAPI(
    title="Money Managing App"
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(currency_router, prefix="/currency", tags=["currency"])
app.include_router(account_router, prefix="/account", tags=["account"])


@app.get("/ping")
async def ping():
    return {"message": "pong"}
