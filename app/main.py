from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

#creating the FastAPI app
app = FastAPI(
    title="📚 Book Tracker API",
    version="1.0.0"
)

#Allowing the dashboard to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Serving dashboard HTML files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/dashboard", include_in_schema=False)
def serve_dashboard():
    return FileResponse("static/dashboard.html")

#temporary database
books_db: dict[int, dict] = {
    1: {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "status": "reading", "progress": 60, "genre": "Tech", "added_at": "2025-01-10T09:00:00"},
    2: {"id": 2, "title": "Atomic Habits", "author": "James Clear", "status": "to-read", "progress": 0, "genre": "Self-Help", "added_at": "2025-02-01T08:00:00"},
      }
next_id = 3

#schemas
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    genre: str = Field(default="General")
    status: str = Field(default="to-read")
    progress: int = Field(default=0, ge=0, le=100)

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = Field(default=None, ge=0, le=100)


#Routes
@app.get("/")
def root():
    return {"message":"📚 Book Tracker API is running!" }

@app.get("/books")
def get_books(status: Optional[str] = None):
    books = list(books_db.values())
    return [b for b in books if b["status"] == status] if status else books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found.")
    return books_db[book_id]

@app.post("/books", status_code=201)
def create_book(book: BookCreate):
    global next_id
    new = {**book.model_dump(), "id": next_id,
           "added_at": datetime.utcnow().isoformat()}
    books_db[next_id] = new
    next_id += 1
    return new

@app.patch("/books/{book_id}")
def update_book(book_id: int, updates: BookUpdate):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found.")
    book = books_db[book_id]
    for field, val in updates.model_dump(exclude_none=True).items():
        book[field] = val
    if book.get("progress") == 100:
        book["status"] = "completed"
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found.")
    del books_db[book_id]
    return {"message": f"Book {book_id} deleted."}

@app.get("/stats")
def get_stats():
    books = list(books_db.values())
    total = len(books)
    return {
        "total":            total,
        "completed":        sum(1 for b in books if b["status"] == "completed"),
        "reading":          sum(1 for b in books if b["status"] == "reading"),
        "to_read":          sum(1 for b in books if b["status"] == "to-read"),
        "average_progress": round(sum(b["progress"] for b in books) / total, 1) if total else 0,
    }
