from http.cookies import SimpleCookie
from typing import AsyncGenerator
import asyncio
from httpx import AsyncClient
import pytest
from sqlalchemy import NullPool, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.config import settings
from src.database import get_async_session
from src.main import app
from src.models import Base, User

# Database
# Creates an asynchronous SQLAlchemy engine for the test database using the URL from the settings object.
test_engine = create_async_engine(settings.db_url, poolclass=NullPool)
# SQLAlchemy session factory using the created test_engine.
test_SessionLocal = sessionmaker(test_engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False)
# Binds the SQLAlchemy models' metadata to the test_engine.
Base.metadata.bind = test_engine


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields:
        AsyncSession: An asynchronous session.
    """
    async with test_SessionLocal() as session:
        yield session


# overrides the dependency get_async_session in the app object with the asynchronous function.
app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    """
    Prepares the database before running tests in the session scope.

    Yields:
        None
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Setup
@pytest.fixture(scope="session")
def event_loop(request):
    """
    Fixture for providing an event loop for the session scope.

    Args:
        request: The request object.

    Yields:
        asyncio.AbstractEventLoop: An event loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client():
    """
    Fixture for providing a test client for the session scope.

    Yields:
        TestClient: A test client instance.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture for providing an asynchronous test client for the session scope.

    Yields:
        AsyncClient: An asynchronous test client instance.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_superuser_cookie():
    client = TestClient(app)
    client.post("/auth/register", json={
        "email": "super@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
    })

    login_response = client.post("/auth/jwt/login", data={
        "username": "super@example.com",
        "password": "string"
    })

    cookies = SimpleCookie(login_response.headers["set-cookie"])

    async with test_SessionLocal() as session:
        stmt = select(User).where(User.email == "super@example.com")
        user = await session.execute(stmt)
        user = user.scalar_one()
        user.is_superuser = True
        await session.commit()

    return {c.key: c.value for c in cookies.values()}


@pytest.fixture(scope="session")
async def authenticated_user_cookie():
    client = TestClient(app)
    client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
    })

    login_response = client.post("/auth/jwt/login", data={
        "username": "user@example.com",
        "password": "string"
    })

    cookies = SimpleCookie(login_response.headers["set-cookie"])

    async with test_SessionLocal() as session:
        stmt = select(User).where(User.email == "user@example.com")
        user = await session.execute(stmt)
        user = user.scalar_one()
        user.is_superuser = True
        await session.commit()

    return {c.key: c.value for c in cookies.values()}
