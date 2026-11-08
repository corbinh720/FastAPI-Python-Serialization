
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()


# Define book and author models
class Author(BaseModel):
    name: str
    email: Optional[str] = None


class Book(BaseModel):
    id: int
    title: str
    author: Author
    year: int
    genre: str
    ratings: List[int] = Field(default_factory=list)


# Model for partial updates
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[Author] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    ratings: Optional[List[int]] = None


# Store books in memory
books = [
    Book(
        id=1,
        title="The Great Gatsby",
        author=Author(
            name="F. Scott Fitzgerald",
            email="fscott@example.com"
        ),
        year=1925,
        genre="Fiction",
        ratings=[5, 4, 5]
    ),
    Book(
        id=2,
        title="1984",
        author=Author(name="George Orwell"),
        year=1949,
        genre="Dystopian",
        ratings=[5, 5, 4]
    )
]


# Get all books
@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books


# Exercise 1: Search by genre
@app.get("/books/genre/{genre}", response_model=List[Book])
async def search_books_by_genre(genre: str):
    return [
        book for book in books
        if book.genre.lower() == genre.lower()
    ]


# Exercise 5: Count books
@app.get("/books/count")
async def count_books():
    return {"count": len(books)}


# Get a book by ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# Exercise 2: Create book with ratings
@app.post("/books", response_model=Book)
async def create_book(book: Book):
    if any(b.id == book.id for b in books):
        raise HTTPException(
            status_code=400,
            detail="Book ID already exists"
        )

    books.append(book)
    return book


# Exercise 2: Update book with ratings
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books):
        if book.id == book_id:
            updated_book.id = book_id
            books[i] = updated_book
            return updated_book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# Exercise 3: Update selected book fields
@app.patch("/books/{book_id}", response_model=Book)
async def patch_book(book_id: int, updates: BookUpdate):
    for i, book in enumerate(books):
        if book.id == book_id:
            update_data = updates.model_dump(
                exclude_unset=True
            )

            updated_book = book.model_copy(
                update=update_data
            )

            books[i] = updated_book
            return updated_book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# Delete a book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            books.pop(i)
            return {"message": "Book deleted"}

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# Start the server
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
