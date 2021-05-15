from datetime import date
from typing import Optional
from pydantic import BaseModel

class ShowBase(BaseModel):
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