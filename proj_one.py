from fastapi import FastAPI,Body

Books = [
    {"id": 1, "title": "HP1", "author": "author1", "year": "1993"},
    {"id": 2, "title": "HP2", "author": "author2", "year": "1994"},
    {"id": 3, "title": "HP3", "author": "author3", "year": "1993"},
    {"id": 4, "title": "HP4", "author": "author1", "year": "1994"},
]

app = FastAPI()

@app.get("/books")
async def get_all_books():
    return Books

@app.get("/books/{book_id}")
async def get_specific_book(book_id):
    for book in Books:
        if book_id in book:
            return book

@app.get("/book/")
async def get_specific_author(author_name: str):
    res = []
    for book in Books:
        if book["author"] == author_name:
            res.append(book)
    return res

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    Books.append(new_book)

@app.put("/book/{book_id}")
async def update_book(book_id: int, updated_book: dict):
    for index, book in enumerate(Books):
        if book["id"] == book_id:
            Books[index].update(updated_book)

        
@app.delete("/book/{book_id}")
async def delete_book(book_id: int):
    for book in Books:
        if book["id"] == book_id:
            Books.remove(book)


