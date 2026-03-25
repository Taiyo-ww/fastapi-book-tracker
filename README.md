# 📚 Student Book Tracker — FastAPI + Dashboard

A beginner-friendly REST API built with **FastAPI** (Python), served alongside a **styled browser dashboard** for tracking books you're reading.

## 🚀 Quick Start

1. Clone the repo
   git clone https://github.com/Taiyo-ww/fastapi-book-tracker.git
   cd fastapi-book-tracker

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Run the server
   uvicorn app.main:app --reload

5. Open your browser
   Dashboard: http://127.0.0.1:8000/dashboard
   API Docs:  http://127.0.0.1:8000/docs

## 🧪 Run Tests
   pytest tests/test_main.py -v

## 📁 Project Structure
   fastapi-book-tracker/
   ├── app/
   │   ├── __init__.py
   │   └── main.py
   ├── static/
   │   └── dashboard.html
   ├── tests/
   │   ├── __init__.py
   │   └── test_main.py
   ├── requirements.txt
   ├── TOOLKIT.md
   └── README.md

## 🔗 API Endpoints
   GET    /              Welcome message
   GET    /books         List all books
   GET    /books/{id}    Single book
   POST   /books         Add a book
   PATCH  /books/{id}    Update progress
   DELETE /books/{id}    Remove a book
   GET    /stats         Reading statistics
   GET    /dashboard     HTML dashboard

## 🛠 Built With
   FastAPI    - API framework
   Pydantic   - Data validation
   Uvicorn    - ASGI server
   HTML/CSS/JS - Zero-dependency dashboard