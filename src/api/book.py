from fastapi import APIRouter, Query, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from src.api.dependencies import AccessTokenBearer
from src.core.db import get_session
from src.model.book import Book
from src.services.book import BookService

router = APIRouter()
books = BookService()
access_token_bearer = AccessTokenBearer()

@router.get("/books", status_code=status.HTTP_200_OK)
async def root(session: AsyncSession = Depends(get_session), user_sec = Depends(access_token_bearer)) :
    result = await books.get_books(session) 
    return result


@router.get('/book/{book_id}', status_code=status.HTTP_200_OK) 
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)) :
    result = await books.get_book(book_id, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return result

@router.post('/books', status_code=status.HTTP_201_CREATED)
async def add_book(book: Book, session: AsyncSession = Depends(get_session)) :
    new_book = await books.create_book(book, session)
    return new_book

@router.put("/book/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_id: str, updated_book: Book, session: AsyncSession = Depends(get_session)):
    result = await books.update_book(book_id, updated_book, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return result

@router.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session)) :
    result = await books.delete_book(book_id, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return JSONResponse(content={"message": "Book deleted successfully"}, status_code=status.HTTP_200_OK)
