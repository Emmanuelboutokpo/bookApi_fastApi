from fastapi import APIRouter, Query, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from src.core.db import get_session
from src.model.model import Book
from src.services.services import BookService

router = APIRouter()
books = BookService()

@router.get("/books")
async def root(session: AsyncSession = Depends(get_session)) :
    result = await books.get_books(session) 
    return result


@router.get('/book/{book_id}') 
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)) :
    result = await books.get_book(book_id, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return result

@router.post('/books')
async def add_book(book: Book, session: AsyncSession = Depends(get_session)) :
    new_book = await books.create_book(book, session)
    return new_book

@router.put("/book/{book_id}")
async def update_book(book_id: str, updated_book: Book, session: AsyncSession = Depends(get_session)):
    result = await books.update_book(book_id, updated_book, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return result

@router.delete("/books/{book_id}")
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session)) :
    result = await books.delete_book(book_id, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return JSONResponse(content={"message": "Book deleted successfully"}, status_code=status.HTTP_200_OK)
