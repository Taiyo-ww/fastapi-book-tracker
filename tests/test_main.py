"""
Tests for the Book Tracker API.
Run with: pytest tests/test_main.py -v
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "Book Tracker" in r.json()["message"]


def test_get_all_books():
    r = client.get("/books")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1


def test_get_single_book():
    r = client.get("/books/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1


def test_404_on_missing_book():
    r = client.get("/books/9999")
    assert r.status_code == 404


def test_create_book():
    r = client.post("/books", json={
        "title": "Deep Work", "author": "Cal Newport",
        "genre": "Self-Help", "status": "to-read", "progress": 0
    })
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Deep Work"
    assert "id" in data


def test_update_progress():
    r = client.patch("/books/1", json={"progress": 75})
    assert r.status_code == 200
    assert r.json()["progress"] == 75


def test_complete_on_100():
    r = client.patch("/books/1", json={"progress": 100})
    assert r.status_code == 200
    assert r.json()["status"] == "completed"


def test_delete_book():
    created = client.post("/books", json={
        "title": "Temp", "author": "Temp Author"
    }).json()
    r = client.delete(f"/books/{created['id']}")
    assert r.status_code == 200
    assert client.get(f"/books/{created['id']}").status_code == 404


def test_stats():
    r = client.get("/stats")
    data = r.json()
    assert "total" in data and "completed" in data and "reading" in data


def test_filter_by_status():
    r = client.get("/books?status=completed")
    assert all(b["status"] == "completed" for b in r.json())