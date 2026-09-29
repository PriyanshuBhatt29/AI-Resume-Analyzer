from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import settings
from .parsers import extract_text
from .scoring import get_matcher

app = FastAPI(
    title="Resume Intelligence API",
    version="1.0.0",
    description="Semantic resume-to-job matching powered by transformer embeddings.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeTextRequest(BaseModel):
    resume_text: str = Field(min_length=20, max_length=settings.max_text_length)
    job_description: str = Field(min_length=20, max_length=settings.max_text_length)

@app.get("/api/health")
def health():
    return {"status": "ok", "model": settings.model_name}

@app.post("/api/analyze")
async def analyze(resume: UploadFile = File(...), job_description: str = ""):
    if not job_description.strip():
        raise HTTPException(status_code=422, detail="Job description is required.")
    data = await resume.read()
    try:
        resume_text = extract_text(resume.filename or "resume.txt", data)
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    if len(resume_text) < 20:
        raise HTTPException(status_code=422, detail="Could not extract enough text from the resume.")
    return get_matcher().analyze(resume_text, job_description)

@app.post("/api/analyze-text")
def analyze_text(payload: AnalyzeTextRequest):
    return get_matcher().analyze(payload.resume_text, payload.job_description)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
