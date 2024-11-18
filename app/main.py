from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, database
from .database import engine, init_db
from .ai_service import generate_words_from_text
from typing import List
import json
import logging

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

#@app.on_event("startup")
#async def startup_event():
#    init_db()  # Thi

@app.get("/")
async def home(request: Request, db: Session = Depends(database.get_db)):
    total_words = db.query(models.Word).count()
    mastered_words = db.query(models.Word).filter(models.Word.status == models.LearningStatus.MASTERED).count()
    need_to_learn = db.query(models.Word).filter(models.Word.status == models.LearningStatus.NEED_TO_LEARN).count()
    not_mastered = db.query(models.Word).filter(models.Word.status == models.LearningStatus.NOT_MASTERED).count()
    
    words = db.query(models.Word).all()
    return templates.TemplateResponse(
        "index.html", {
            "request": request, 
            "words": words,
            "total_words": total_words,
            "mastered_words": mastered_words,
            "need_to_learn": need_to_learn,
            "not_mastered": not_mastered
        }
    )

@app.get("/words/{status}")
async def filtered_words(request: Request, status: str, db: Session = Depends(database.get_db)):
    if status == "all":
        words = db.query(models.Word).all()
        return templates.TemplateResponse("words.html", {"request": request, "words": words})
    elif status == "addword":
        return templates.TemplateResponse("add_word.html", {"request": request})
    else:
        words = db.query(models.Word).filter(models.Word.status == models.LearningStatus(status)).all()
    return templates.TemplateResponse(
        "words_card.html", 
        {
            "request": request, 
            "words": words,
            "current_index": 0 if words else -1,
            "total_words": len(words)
        }
    ) 

@app.post("/add_word")
async def add_word(
    word: str = Form(...),
    explanation: str = Form(...),
    example: str = Form(...),
    db: Session = Depends(database.get_db)
):
    db_word = models.Word(
        word=word,
        explanation=explanation,
        example=example,
        status=models.LearningStatus.NOT_MASTERED
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return {"success": True}

@app.post("/update_status/{word_id}")
async def update_status(
    word_id: int,
    status: str = Form(...),
    db: Session = Depends(database.get_db)
):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    word.status = models.LearningStatus(status)
    db.commit()
    return {"success": True}

@app.post("/update_word/{word_id}")
async def update_word(
    word_id: int,
    word: str = Form(...),
    explanation: str = Form(...),
    example: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(database.get_db)
):
    db_word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    db_word.word = word
    db_word.explanation = explanation
    db_word.example = example
    db_word.status = models.LearningStatus(status)
    db.commit()
    return {"success": True}

@app.post("/generate_words")
async def generate_words(
    text: str = Form(...),
):
    try:
        generated_words = await generate_words_from_text(text)
        return generated_words
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete_word/{word_id}")
async def delete_word(
    word_id: int,
    db: Session = Depends(database.get_db)
):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    db.delete(word)
    db.commit()
    return {"success": True}
