from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings
import os

# Use environment variable to determine if we're in test mode
is_test = os.environ.get("TESTING", "0") == "1"

# Use SQLite for tests, PostgreSQL for production
if is_test:
    async_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
else:
    async_engine = create_async_engine(settings.SUPABASE_DB_URL, echo=True)

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
