from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from db import books
from schema import Book

app = FastAPI()

@app.get("/books")
async def root(sorted_by: str = Query(default=None, description="sort by field", examples="title, author, publisher, published_date, language"),
            order: str = Query("asc", description="sort order", examples="asc, desc")) :
    
    result = books
    if sorted_by is not None :
        if sorted_by not in ['id', 'title', 'author', 'publisher', 'published_date', 'language'] :
           raise HTTPException(status_code=400, detail="Invalid sort field")
    
        if order not in ['asc', 'desc'] :
           raise HTTPException(status_code=400, detail="Invalid sort order")

        sorted_orders = False if order == 'desc' else True
        result = sorted(books, key=lambda x: x[sorted_by], reverse=sorted_orders) 

    return JSONResponse(content=result, status_code=200)


@app.get('/book/{book_id}') 
async def get_book(book_id: int) :
    for book in books : 
        if book['id'] == book_id :
            return JSONResponse(content=book, status_code=200)
    raise HTTPException(status_code=404, detail="Book not found")


@app.post('/books')
async def add_book(book: Book) :
    new_book = book.model_dump()
    new_book['id'] = max(book['id'] for book in books) + 1
    books.append(new_book)
    return JSONResponse(content={"message": "Book added successfully", "book": new_book}, status_code=201)



@app.put("/book/{book_id}")
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book['id'] == book_id:
            updated_dict = updated_book.model_dump(exclude_unset=True)
            book.update(updated_dict)
            book['id'] = book_id
            return JSONResponse(content={"message": "Book updated successfully"}, status_code=200)
    
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int) :
    for index, book in enumerate(books) :
        if book['id'] == book_id :
            del books[index]
            return JSONResponse(content={"message": "Book deleted successfully"}, status_code=200)
    raise HTTPException(status_code=404, detail="Book not found")
