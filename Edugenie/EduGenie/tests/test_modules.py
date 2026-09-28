import pytest

from app import qna, summary_module, learning_path


@pytest.mark.anyio
async def test_qna_prompt(monkeypatch):
    captured = {}

    def fake_generate(prompt, **kwargs):
        captured["prompt"] = prompt
        return "answer"

    monkeypatch.setattr(qna, "generate_text", fake_generate)
    result = await qna.answer_question("What is gravity?")
    assert result == "answer"
    assert "What is gravity?" in captured["prompt"]


@pytest.mark.anyio
async def test_summary(monkeypatch):
    monkeypatch.setattr(summary_module, "generate_text", lambda *a, **k: "summary")
    assert await summary_module.summarize_text("long text") == "summary"


@pytest.mark.anyio
async def test_learning_path(monkeypatch):
    monkeypatch.setattr(learning_path, "generate_text", lambda *a, **k: "learning path")
    assert await learning_path.get_learning_recommendations("SQL") == "learning path"
