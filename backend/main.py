from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from groq import Groq
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime
import os
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    selected_text = Column(Text)
    note_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class QuizResult(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True)
    selected_text = Column(Text)
    score = Column(Integer)
    total = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="AI Learning Companion API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Something went wrong. Please try again."}
    )

class TextRequest(BaseModel):
    text: str

    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty')
        if len(v.strip()) < 10:
            raise ValueError('Text too short — please select more text')
        return v.strip()

class NoteRequest(BaseModel):
    selected_text: str
    note_text: str

    @validator('note_text')
    def note_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Note cannot be empty')
        return v.strip()

class QuizResultRequest(BaseModel):
    selected_text: str
    score: int
    total: int

@app.get("/")
def health_check():
    logger.info("Health check called")
    return {"status": "ok", "message": "AI Learning Companion API is running"}

@app.post("/api/explain")
@limiter.limit("10/minute")
async def explain_text(request: Request, body: TextRequest):
    try:
        logger.info(f"Explain request: {len(body.text)} chars")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""Explain the following text in simple, easy-to-understand language.
                Use bullet points and keep it concise.
                Text: {body.text}"""
            }]
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        logger.error(f"Explain error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/summary")
@limiter.limit("10/minute")
async def summary_text(request: Request, body: TextRequest):
    try:
        logger.info(f"Summary request: {len(body.text)} chars")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""Summarize the following text in 3-5 bullet points.
                Be concise and capture the main ideas.
                Text: {body.text}"""
            }]
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        logger.error(f"Summary error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/quiz")
@limiter.limit("10/minute")
async def quiz_text(request: Request, body: TextRequest):
    try:
        logger.info(f"Quiz request: {len(body.text)} chars")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""You are a quiz generator. Generate exactly 3 multiple choice questions based on the text below.

IMPORTANT: Return ONLY a valid JSON object. No explanation, no markdown, no code fences. Just raw JSON.

Return this exact structure:
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": ["A) option one", "B) option two", "C) option three", "D) option four"],
      "answer": "A",
      "explanation": "Why A is correct"
    }}
  ]
}}

Text: {body.text}"""
            }]
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        data = json.loads(raw)
        return data
    except Exception as e:
        logger.error(f"Quiz error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/quiz/result")
async def save_quiz_result(request: Request, body: QuizResultRequest):
    try:
        db = SessionLocal()
        result = QuizResult(
            selected_text=body.selected_text,
            score=body.score,
            total=body.total
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        db.close()
        logger.info(f"Quiz result saved: {body.score}/{body.total}")
        return {"id": result.id, "message": "Quiz result saved!"}
    except Exception as e:
        logger.error(f"Save quiz result error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/quiz/results")
async def get_quiz_results():
    try:
        db = SessionLocal()
        results = db.query(QuizResult).order_by(
            QuizResult.created_at.desc()
        ).limit(10).all()
        db.close()
        return {"results": [
            {
                "id": r.id,
                "selected_text": r.selected_text,
                "score": r.score,
                "total": r.total,
                "created_at": str(r.created_at)
            } for r in results
        ]}
    except Exception as e:
        logger.error(f"Get quiz results error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/notes")
@limiter.limit("20/minute")
async def save_note(request: Request, body: NoteRequest):
    try:
        db = SessionLocal()
        note = Note(
            selected_text=body.selected_text,
            note_text=body.note_text
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        db.close()
        logger.info(f"Note saved: id={note.id}")
        return {"id": note.id, "message": "Note saved!"}
    except Exception as e:
        logger.error(f"Save note error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/notes")
async def get_notes():
    try:
        db = SessionLocal()
        notes = db.query(Note).order_by(Note.created_at.desc()).all()
        db.close()
        return {"notes": [
            {
                "id": n.id,
                "selected_text": n.selected_text,
                "note_text": n.note_text,
                "created_at": str(n.created_at)
            } for n in notes
        ]}
    except Exception as e:
        logger.error(f"Get notes error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/api/notes/{note_id}")
async def delete_note(note_id: int):
    try:
        db = SessionLocal()
        note = db.query(Note).filter(Note.id == note_id).first()
        if note:
            db.delete(note)
            db.commit()
        db.close()
        logger.info(f"Note deleted: id={note_id}")
        return {"message": "Note deleted!"}
    except Exception as e:
        logger.error(f"Delete note error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/dashboard")
async def get_dashboard():
    try:
        db = SessionLocal()
        total_notes = db.query(Note).count()
        total_quizzes = db.query(QuizResult).count()
        avg_score = db.query(QuizResult).all()
        
        if avg_score:
            average = sum(r.score for r in avg_score) / len(avg_score)
        else:
            average = 0

        recent_notes = db.query(Note).order_by(
            Note.created_at.desc()
        ).limit(5).all()
        
        recent_quizzes = db.query(QuizResult).order_by(
            QuizResult.created_at.desc()
        ).limit(5).all()
        
        db.close()
        return {
            "stats": {
                "total_notes": total_notes,
                "total_quizzes": total_quizzes,
                "average_score": round(average, 1)
            },
            "recent_notes": [
                {
                    "id": n.id,
                    "selected_text": n.selected_text,
                    "note_text": n.note_text,
                    "created_at": str(n.created_at)
                } for n in recent_notes
            ],
            "recent_quizzes": [
                {
                    "id": r.id,
                    "score": r.score,
                    "total": r.total,
                    "created_at": str(r.created_at)
                } for r in recent_quizzes
            ]
        }
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})