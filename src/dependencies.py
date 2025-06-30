from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import async_engine

# Async dependency
async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session