from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.api_v1.routers import all_routers
# from src.app.router import currency_router, account_router, category_router, sub_category_router, savings_account_router

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

for router in all_routers:
    app.include_router(router)

# app.include_router(currency_router, prefix="/currency", tags=["currency"])
# app.include_router(savings_account_router, prefix="/savings_account", tags=["savings-account"])
# app.include_router(category_router, prefix="/category", tags=["category"])
# app.include_router(sub_category_router, prefix="/sub_category", tags=["sub-category"])
#

@app.get("/ping")
async def ping():
    return {"message": "pong"}
