from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_chat():
    response = client.post(
        "/chat",
        json={"message": "Hello", "history": []},
    )
    assert response.status_code == 200
    assert "response" in response.json()

def test_summarize():
    response = client.post(
        "/summarize",
        json={"text": "Artificial intelligence helps developers."},
    )
    assert response.status_code == 200
    assert "response" in response.json()

def test_rewrite():
    response = client.post(
        "/rewrite",
        json={
            "text": "Send me the report.",
            "style": "professional",
        },
    )
    assert response.status_code == 200
    assert "response" in response.json()

def test_extract():
    response = client.post(
        "/extract",
        json={
            "text": "Rahul will finish the API by Friday."
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "people" in data
    assert "tasks" in data
    assert "events" in data

def test_generate():
    response = client.post(
        "/generate",
        json={
            "instruction": "Write a one sentence greeting."
        },
    )
    assert response.status_code == 200
    assert "response" in response.json()