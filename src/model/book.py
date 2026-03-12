import uuid
from typing import Optional, List
from src.schemas.review import Review
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime, func
from datetime import datetime
from src.model.user import User

class Book(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    author: str
    publisher: str
    published_date: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: datetime = Field( sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
    
    owner: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}', publisher='{self.publisher}', published_date='{self.published_date}', page_count={self.page_count}, language='{self.language}')"
 