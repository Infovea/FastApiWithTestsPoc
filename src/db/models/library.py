from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .book import Book

class Library(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True, index=True)
    name: str
    location: str
    books: List["Book"] = Relationship(back_populates="library")
