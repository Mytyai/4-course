from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Создание приложения FastAPI
app = FastAPI(
    title="Books API",
    description="REST API для управления библиотекой книг",
    version="1.0.0"
)

# Модель данных для книги
class Book(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200, description="Название книги")
    author: str = Field(..., min_length=1, max_length=100, description="Автор книги")
    year: int = Field(..., ge=1000, le=datetime.now().year, description="Год издания")
    isbn: Optional[str] = Field(None, min_length=10, max_length=13, description="ISBN книги")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Мастер и Маргарита",
                "author": "Михаил Булгаков",
                "year": 1967,
                "isbn": "9785170123456"
            }
        }

# Модель для частичного обновления книги
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)

# Временное хранилище данных
books_db: List[Book] = [
    Book(id=1, title="Война и мир", author="Лев Толстой", year=1869, isbn="9785170987654"),
    Book(id=2, title="Преступление и наказание", author="Федор Достоевский", year=1866, isbn="9785170876543"),
    Book(id=3, title="Евгений Онегин", author="Александр Пушкин", year=1833, isbn="9785170765432")
]

# Счетчик для генерации ID
next_id = 4

# Корневой эндпоинт
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Добро пожаловать в Books API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Получение всех книг
@app.get("/api/books", response_model=List[Book], tags=["Books"])
async def get_books():
    return books_db

# Получение книги по ID
@app.get("/api/books/{book_id}", response_model=Book, tags=["Books"])
async def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Книга с ID {book_id} не найдена")

# Создание новой книги
@app.post("/api/books", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
async def create_book(book: Book):
    global next_id
    book.id = next_id
    next_id += 1
    books_db.append(book)
    return book

# Полное обновление книги
@app.put("/api/books/{book_id}", response_model=Book, tags=["Books"])
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            updated_book.id = book_id
            books_db[index] = updated_book
            return updated_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Книга с ID {book_id} не найдена")

# Частичное обновление книги
@app.patch("/api/books/{book_id}", response_model=Book, tags=["Books"])
async def partial_update_book(book_id: int, book_update: BookUpdate):
    for book in books_db:
        if book.id == book_id:
            update_data = book_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(book, field, value)
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Книга с ID {book_id} не найдена")

# Удаление книги
@app.delete("/api/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
async def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Книга с ID {book_id} не найдена")

# Точка входа
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
