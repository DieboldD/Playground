from datetime import date
from typing import Optional
from pydantic import BaseModel

class ShowBase(BaseModel):
    """
    Standard response schema.
    """
    id: int
    show_id: str
    type: str
    title: str
    director: Optional[str] = None
    cast: Optional[str] = None
    country: str
    date_added: date
    release_year: int
    rating: str
    duration: str
    listed_in: str
    description: Optional[str] = None
    class Config:
        orm_mode=True

class ShowCreate(BaseModel):
    """
    Create Schema based upon the dataset:
    Since we don't know if Netflix would ever change or alter their ID paradigm, we need to respect it's a string.
    """
    show_id: str
    type: str
    title: str
    director: Optional[str] = None
    cast: Optional[str] = None
    country: str
    date_added: date
    release_year: int
    rating: str
    duration: str
    listed_in: str
    description: Optional[str] = None
    class Config:
        orm_mode=True

