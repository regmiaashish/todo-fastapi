from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from dotenv import load_dotenv
import os

from . import models, schemas, auth
from .database import SessionLocal, engine, get_db

# Load environment variables
load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()



# ---------- Auth Endpoints ----------


@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = auth.get_password_hash(user.password)

    # Create new user
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ---------- Todo Endpoints ----------

@app.get("/todos", response_model=list[schemas.Todo])
def get_todos(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()

@app.post("/todos", response_model=schemas.Todo)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_todo = models.Todo(**todo.dict(), user_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(
    todo_id: int,
    todo: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.user_id == current_user.id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.task is not None:
        db_todo.task = todo.task
    if todo.completed is not None:
        db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.user_id == current_user.id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"ok": True}