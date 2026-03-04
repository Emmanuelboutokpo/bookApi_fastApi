from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import datetime
import uuid

class Book(BaseModel):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, description="The unique identifier for the book")
    title : Annotated[str, Field(description="The title of the book")]
    author : Annotated[str, Field(description="The author of the book")]
    publisher : Annotated[str, Field(description="The publisher of the book")]
    published_date : Annotated[datetime, Field(description="The published date of the book in YYYY-MM-DD format")]
    page_count : Annotated[int, Field(description="The number of pages in the book")]   
    language : Annotated[str, Field(description="The language of the book")]
    created_at : Annotated[datetime, Field(description="The date and time when the book was created")]
    updated_at : Annotated[datetime, Field(description="The date and time when the book was last updated")]


class BookSchema(BaseModel):
    title : Annotated[str, Field(description="The title of the book")]
    author : Annotated[str, Field(description="The author of the book")]
    publisher : Annotated[str, Field(description="The publisher of the book")]
    published_date : Annotated[datetime, Field(description="The published date of the book in YYYY-MM-DD format")]
    page_count : Annotated[int, Field(description="The number of pages in the book")]   
    language : Annotated[str, Field(description="The language of the book")]