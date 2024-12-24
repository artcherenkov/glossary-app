# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas, crud

# Создадим таблицы (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Glossary API",
              description="Простое приложение для работы с терминами в глоссарии",
              version="1.0.0")


# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Получить список всех терминов
@app.get("/terms", response_model=list[schemas.TermOut])
def read_terms(db: Session = Depends(get_db)):
    terms = crud.get_terms(db)
    return terms

# 2. Получить конкретный термин по ключу
@app.get("/terms/{term_key}", response_model=schemas.TermOut)
def read_term(term_key: str, db: Session = Depends(get_db)):
    db_term = crud.get_term_by_key(db, term_key)
    if not db_term:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Термин не найден")
    return db_term

# 3. Добавить новый термин
@app.post("/terms", response_model=schemas.TermOut, status_code=status.HTTP_201_CREATED)
def create_new_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    existing_term = crud.get_term_by_key(db, term.key)
    if existing_term:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Термин с таким ключом уже существует")
    db_term = crud.create_term(db, term)
    return db_term

# 4. Обновить существующий термин
@app.put("/terms/{term_key}", response_model=schemas.TermOut)
def update_existing_term(term_key: str, new_data: schemas.TermUpdate, db: Session = Depends(get_db)):
    db_term = crud.get_term_by_key(db, term_key)
    if not db_term:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Термин не найден")
    updated = crud.update_term(db, db_term, new_data)
    return updated

# 5. Удалить термин
@app.delete("/terms/{term_key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_term(term_key: str, db: Session = Depends(get_db)):
    db_term = crud.get_term_by_key(db, term_key)
    if not db_term:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Термин не найден")
    crud.delete_term(db, db_term)
    return None
