from pydantic import BaseModel, Field
from typing import Optional, Annotated

class Book(BaseModel):
    id : Annotated[Optional[int], Field(default=None, description="The unique identifier of the book")]
    title : Annotated[str, Field(description="The title of the book")]
    author : Annotated[str, Field(description="The author of the book")]
    publisher : Annotated[str, Field(description="The publisher of the book")]
    published_date : Annotated[str, Field(description="The published date of the book in YYYY-MM-DD format")]
    page_count : Annotated[int, Field(description="The number of pages in the book")]   
    language : Annotated[str, Field(description="The language of the book")]
    