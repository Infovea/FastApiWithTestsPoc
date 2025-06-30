from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Book(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True, index=True)
    title: str
    author: str
    year: int
    library_id: Optional[int] = Field(default=None, foreign_key="library.id")
    library: Optional["Library"] = Relationship(back_populates="books")
