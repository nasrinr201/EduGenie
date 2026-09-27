from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="AI-powered Learning Assistant",
    version="1.0"
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")


class TextRequest(BaseModel):
    text: str


class QuestionRequest(BaseModel):
    question: str


class QuizRequest(BaseModel):
    text: str
    count: int = 3


class LearningRequest(BaseModel):
    topic: str
    level: str = "beginner"


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/qa")
def qa(request: QuestionRequest):
    try:
        return {"answer": answer_question(request.question)}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/explain")
def explain(request: TextRequest):
    try:
        return {"explanation": explain_topic(request.text)}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/quiz")
def quiz(request: QuizRequest):
    try:
        return {"quiz": generate_quiz(request.text, request.count)}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/summarize")
def summarize(request: TextRequest):
    try:
        return {
            "original_text": request.text,
            "summary": summarize_text(request.text)
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/learn/recommendations")
def learning_recommendations(request: LearningRequest):
    try:
        return {
            "learning_path": get_learning_recommendations(
                request.topic,
                request.level
            )
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/api")
def api_status():
    return {
        "message": "EduGenie API is running!",
        "features": [
            "Question & Answer",
            "Explain Topic",
            "Generate Quiz",
            "Summarize Notes",
            "Learning Path"
        ]
    }