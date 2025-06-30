from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from src.dependencies import get_async_session  # Import from dependencies instead

router = APIRouter(
    prefix="/book",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Book)
async def create_book(book: Book, session: AsyncSession = Depends(get_async_session)):
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book

@router.get("/", response_model=list[Book])
async def get_books(session: AsyncSession = Depends(get_async_session), skip: int = 0, limit: int = 100):
    result = await session.exec(select(Book).offset(skip).limit(limit))
    books = result.all()
    return books

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, book_data: Book, session: AsyncSession = Depends(get_async_session)):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for field, value in book_data.model_dump().items():
        setattr(book, field, value)

    await session.commit()
    await session.refresh(book)
    return book

