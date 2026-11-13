import json
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="FastAPIpractice",
    description="First FastAPI application",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. Модель данных
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    price: float
    in_stock: bool

# 2. Загрузка данных
with open("src/papka/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Функция сохранения
def save_data():
    with open("src/papka/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- МЕТОДЫ ---

@app.get("/books", response_model=list[Book])
async def get_books():
    return data["books"]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.post("/books", response_model=Book)
async def add_book(new_book: Book):
    for book in data["books"]:
        if book["id"] == new_book.id:
            raise HTTPException(status_code=400, detail="Книга с таким ID уже существует")
    data["books"].append(new_book.model_dump())
    save_data()
    return new_book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(data["books"]):
        if book["id"] == book_id:
            deleted_book = data["books"].pop(index)
            save_data()
            return {"message": f"Книга '{deleted_book['title']}' удалена"}
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(data["books"]):
        if book["id"] == book_id:
            data["books"][index] = updated_book.model_dump()
            save_data()
            return updated_book
    raise HTTPException(status_code=404, detail="Книга не найдена")

# 3. Запуск
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)