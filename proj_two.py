from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

class Book(BaseModel):
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: str = Field(gt=1990,lt=2026)

books_db: List[Book] = [
    Book(id=1, title="HP1", author="author1", year="1993"),
    Book(id=2, title="HP2", author="author2", year="1994"),
    Book(id=3, title="HP3", author="author3", year="1993"),
    Book(id=4, title="HP4", author="author1", year="1994"),
]

app = FastAPI()

@app.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    return books_db

@app.get("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_specific_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found"
    )

@app.get("/book/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_books_by_author(author_name: str):
    res = [book for book in books_db if book.author == author_name]
    
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No books found for author '{author_name}'"
        )
    
    return res

@app.post("/books/create_book", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(new_book: Book):
    for book in books_db:
        if book.id == new_book.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with id {new_book.id} already exists"
            )
    
    books_db.append(new_book)
    return new_book

@app.put("/book/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db[index] = updated_book
            return books_db[index]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found"
    )

@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            books_db.remove(book)
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found"
    )