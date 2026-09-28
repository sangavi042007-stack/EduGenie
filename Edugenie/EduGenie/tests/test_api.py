from fastapi.testclient import TestClient
import main
import pytest


client = TestClient(main.app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation():
    response = client.post("/qa", json={"text": ""})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_qa(monkeypatch):
    async def fake(question):
        return "The Pacific Ocean is the largest ocean."

    monkeypatch.setattr(main, "answer_question", fake)
    response = client.post("/qa", json={"text": "Which is the largest ocean?"})
    assert response.status_code == 200
    assert "Pacific" in response.json()["result"]


@pytest.mark.anyio
async def test_quiz(monkeypatch):
    async def fake(text, question_count):
        return {
            "questions": [{
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4"
            }]
        }

    monkeypatch.setattr(main, "generate_quiz", fake)
    response = client.post("/quiz", json={"text": "Basic arithmetic", "question_count": 1})
    assert response.status_code == 200
    assert response.json()["result"]["questions"][0]["correct_answer"] == "4"
