# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def get_terms(db: Session):
    return db.query(models.Term).all()

def get_term_by_key(db: Session, term_key: str):
    return db.query(models.Term).filter(models.Term.key == term_key).first()

def create_term(db: Session, term: schemas.TermCreate):
    db_term = models.Term(key=term.key, description=term.description)
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

def update_term(db: Session, db_term: models.Term, new_data: schemas.TermUpdate):
    db_term.description = new_data.description
    db.commit()
    db.refresh(db_term)
    return db_term

def delete_term(db: Session, db_term: models.Term):
    db.delete(db_term)
    db.commit()
    return True
