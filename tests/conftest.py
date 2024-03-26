from typing import AsyncGenerator
import asyncio
from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.database import get_async_session
from src.main import app
from src.models import Base

# Database
# Creates an asynchronous SQLAlchemy engine for the test database using the URL from the settings object.
test_engine = create_async_engine(settings.db_url)
# SQLAlchemy session factory using the created test_engine.
SessionLocal = sessionmaker(test_engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False)
# Binds the SQLAlchemy models' metadata to the test_engine.
Base.metadata.bind = test_engine


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Setup
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
