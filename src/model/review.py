import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from src.model.user import User
from src.model.book import Book

class Review(SQLModel, table=True):
    uid: uuid.UUID = Field( default_factory=uuid.uuid4, primary_key=True, nullable=False)
    rating: int = Field(ge=1, le=5)
    review_text: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="book.id")

    book: Optional["Book"] = Relationship(back_populates="reviews")
    user: Optional["User"] = Relationship(back_populates="reviews")
