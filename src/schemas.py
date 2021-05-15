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

class ShowSearch(BaseModel):
    show_id: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    director: Optional[str] = None
    cast: Optional[str] = None
    country: Optional[str] = None
    date_added:  Optional[date] = None
    release_year:  Optional[int] = None
    rating:  Optional[str] = None
    duration:  Optional[str] = None
    listed_in:  Optional[str] = None
    description: Optional[str] = None
    class Config:
        orm_mode=True

class SearchSchema(BaseModel):
    """
    Search model with additional fields for simple pagination
    If results are limited, but page number is not supplied, only the first page will be returned.
    """
    criteria:ShowSearch
    max_results:Optional[int]=None
    results_per_page:Optional[int]=None
    page_number:Optional[int]=1
    class Config:
        orm_mode=True
