from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Library, Book
from src.dependencies import get_async_session  # Import from dependencies instead

router = APIRouter(
    prefix="/library",
    tags=["libraries"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Library)
async def create_library(library: Library, session: AsyncSession = Depends(get_async_session)):
    session.add(library)
    await session.commit()
    await session.refresh(library)
    return library

@router.get("/", response_model=list[Library])
async def get_libraries(session: AsyncSession = Depends(get_async_session)):
    result = await session.exec(select(Library))
    libraries = result.all()
    return libraries

@router.get("/{library_id}", response_model=Library)
async def get_library(library_id: int, session: AsyncSession = Depends(get_async_session)):
    library = await session.get(Library, library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    return library

@router.get("/{library_id}/books", response_model=list[Book])
async def get_library_books(library_id: int, session: AsyncSession = Depends(get_async_session)):
    library = await session.get(Library, library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")

    result = await session.exec(select(Book).where(Book.library_id == library_id))
    books = result.all()
    return books

