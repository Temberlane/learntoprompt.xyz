from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, Base, engine
from app.models import Prompt
from app.schemas import PromptCreate, PromptRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="LearnToPrompt API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/prompts", response_model=List[PromptRead])
def list_prompts(db: Session = Depends(get_db)):
    return db.query(Prompt).all()


@app.post("/prompts", response_model=PromptRead, status_code=201)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    db_prompt = Prompt(title=prompt.title, content=prompt.content)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


@app.get("/prompts/{prompt_id}", response_model=PromptRead)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt
