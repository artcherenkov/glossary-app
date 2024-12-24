# app/schemas.py

from pydantic import BaseModel

class TermBase(BaseModel):
    key: str
    description: str | None = None

class TermCreate(TermBase):
    """
    Дополнительные поля, если нужны при создании.
    Пока что можем использовать то же, что в Base.
    """
    pass

class TermUpdate(BaseModel):
    description: str | None = None

class TermOut(TermBase):
    id: int

    class Config:
        orm_mode = True
