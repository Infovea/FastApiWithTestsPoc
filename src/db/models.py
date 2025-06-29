from sqlmodel import SQLModel, Field
from typing import Optional

class Book(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True, index=True)
    title: str
    author: str
    year: int
