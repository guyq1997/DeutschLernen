from fastapi import FastAPI, Request, Form, Depends, HTTPException, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, database
from .database import engine, init_db, upload_db_to_s3
from .ai_service import generate_words_from_text
from typing import List
import json
import logging
from datetime import datetime, time, timedelta
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # This is the correct place to initialize the database
        logging.info("Initializing database tables...")
        models.Base.metadata.create_all(bind=engine)
        
        # Start the backup task
        logging.info("Starting database backup task...")
        backup_task = asyncio.create_task(backup_database())
        
        # Store the task in app state to prevent it from being garbage collected
        app.state.backup_task = backup_task
        
        yield
    except Exception as e:
        logging.error(f"Error during startup: {str(e)}")
        raise
    finally:
        # Cleanup when the application shuts down
        logging.info("Shutting down application...")
        if hasattr(app.state, 'backup_task'):
            app.state.backup_task.cancel()
            try:
                await app.state.backup_task
            except asyncio.CancelledError:
                logging.info("Backup task cancelled successfully")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Global variable to track if backup is running
is_backup_running = False

async def backup_database():
    global is_backup_running
    while True:
        now = datetime.now()
        # Schedule backup for 3 AM
        target_time = time(hour=3, minute=0)
        
        if now.time() >= target_time:
            # Calculate time until next backup (tomorrow at 3 AM)
            tomorrow = now + timedelta(days=1)
            next_backup = datetime.combine(tomorrow.date(), target_time)
        else:
            # Calculate time until next backup (today at 3 AM)
            next_backup = datetime.combine(now.date(), target_time)
        
        # Calculate seconds until next backup
        seconds_until_backup = (next_backup - now).total_seconds()
        
        # Wait until next backup time
        await asyncio.sleep(seconds_until_backup)
        
        # Perform backup
        if not is_backup_running:
            is_backup_running = True
            try:
                upload_db_to_s3()
            finally:
                is_backup_running = False

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
