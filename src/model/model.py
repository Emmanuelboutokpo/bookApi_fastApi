from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, func
from datetime import datetime
import uuid

class Book(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: datetime = Field( sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
    
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}', publisher='{self.publisher}', published_date='{self.published_date}', page_count={self.page_count}, language='{self.language}')"
 