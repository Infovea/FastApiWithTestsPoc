import asyncio
import pytest
import pytest_asyncio
import os
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi.testclient import TestClient
from src.db.models import Book, Library

# Set testing environment variable
os.environ["TESTING"] = "1"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    # Import here to avoid circular imports
    from src.db.main import async_engine

    # Create tables
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield async_engine

    # Drop tables
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest_asyncio.fixture
async def test_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(test_engine) as session:
        yield session

@pytest.fixture
def client():
    # Import here to avoid circular imports
    from src.main import app
    from src.dependencies import get_async_session
    from src.db.main import async_engine

    with TestClient(app) as test_client:
        # Override the get_async_session dependency
        async def get_test_session():
            async with AsyncSession(async_engine) as session:
                yield session

        app.dependency_overrides[get_async_session] = get_test_session

        yield test_client

        # Clean up
        app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def sample_book(test_session: AsyncSession) -> Book:
    book = Book(title="Test Book", author="Test Author", year=2023)
    test_session.add(book)
    await test_session.commit()
    await test_session.refresh(book)
    return book  # Use return instead of yield for simplicity

@pytest_asyncio.fixture
async def sample_library(test_session: AsyncSession) -> Library:
    from src.db.models import Library

    library = Library(name="Test Library", location="Test Location")
    test_session.add(library)
    await test_session.commit()
    await test_session.refresh(library)
    return library

@pytest_asyncio.fixture
async def sample_book_in_library(test_session: AsyncSession, sample_library: Library) -> Book:
    book = Book(
        title="Test Book in Library",
        author="Test Author",
        year=2023,
        library_id=sample_library.id
    )
    test_session.add(book)
    await test_session.commit()
    await test_session.refresh(book)
    return book


