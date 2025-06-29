from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import create_db_and_tables, async_engine
from src.db.models import Book

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    await create_db_and_tables() # Create database and tables if they don't exist
    yield
    # Shutdown
    print("Shutting down...")

# Async dependency
async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session

app = FastAPI(
    debug=True,
    title="Book Service",
    version="0.1.0",
    description="A simple book service",
    lifespan=lifespan,
)


@app.post("/book", response_model=Book)
async def create(book: Book, session: AsyncSession = Depends(get_async_session)):
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book

@app.put("/book/{book_id}", response_model=Book)
async def update(book_id: int, book_data: Book, session: AsyncSession = Depends(get_async_session)):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # We can update individual fields like the following:
    # book.title = book.title
    # book.author = book.author
    # book.year = book.year

    # Or we can update all fields like the following:
    for field, value in book_data.model_dump().items():
        setattr(book, field, value)

    await session.commit()
    await session.refresh(book)
    return book


@app.get("/book")
async def get_books(session: AsyncSession = Depends(get_async_session), skip: int = 0, limit: int = 100):
    result = await session.exec(select(Book).offset(skip).limit(limit))
    books = result.all()
    return books

@app.get("/book/{book_id}", response_model=Book)
async def get_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    # result = await session.exec(select(Book).where(Book.id == book_id))
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
