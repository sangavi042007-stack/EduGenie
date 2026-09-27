from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import TextRequest, QuizRequest
from app.qna import answer_question
from app.explanation_module import explain_topic
from app.quiz_module import generate_quiz
from app.summary_module import summarize_text
from app.learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": "EduGenie"},
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: TextRequest):
    return {"result": await answer_question(payload.text)}


@app.post("/explain")
async def explain(payload: TextRequest):
    return {"result": await explain_topic(payload.text)}


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    return {"result": await generate_quiz(payload.text, payload.question_count)}


@app.post("/summarize")
async def summarize(payload: TextRequest):
    return {"result": await summarize_text(payload.text)}


@app.post("/learn/recommendations")
async def learning_recommendations(payload: TextRequest):
    return {"result": await get_learning_recommendations(payload.text)}
