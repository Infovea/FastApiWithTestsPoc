from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import create_db_and_tables
# from src.dependencies import get_async_session

# Move router imports to the top of the file
from src.routers import books, libraries

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    await create_db_and_tables() # Create database and tables if they don't exist
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    debug=True,
    title="Book Service",
    version="0.1.0",
    description="A simple book service",
    lifespan=lifespan,
)

# Include routers
app.include_router(books.router)
app.include_router(libraries.router)
