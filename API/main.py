from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

# Allow frontend (Angular)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE SETUP (SQLite) ---
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(255))

Base.metadata.create_all(bind=engine)

# --- API ENDPOINTS ---

@app.get("/get_tasks")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    return [{"id": t.id, "task": t.task} for t in tasks]

@app.post("/add_task")
def add_task(task: str = Form(...)):
    db = SessionLocal()
    new_task = Task(task=task)
    db.add(new_task)
    db.commit()
    db.close()
    return {"message": "Task added"}

@app.post("/delete_task")
def delete_task(id: int = Form(...)):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == id).first()
    if task:
        db.delete(task)
        db.commit()
    db.close()
    return {"message": "Task deleted"}
