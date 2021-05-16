from datetime import date
from typing import Optional
from pydantic import BaseModel, constr

class ShowBase(BaseModel):
    """
    Standard response schema.
    """
    id: int
    show_id: constr(max_length=50)
    type: constr(max_length=50)
    title: constr(max_length=200)
    director: Optional[constr(max_length=300)] = ""
    cast: Optional[constr(max_length=1000)] = ""
    country: constr(max_length=200)
    date_added: date
    release_year: int
    rating: constr(max_length=20)
    duration: constr(max_length=20)
    listed_in: constr(max_length=500)
    description: Optional[constr(max_length=2000)] = ""
    class Config:
        orm_mode=True

class ShowCreate(BaseModel):
    """
    Create Schema based upon the dataset:
    Since we don't know if Netflix would ever change or alter their ID paradigm, we need to respect it's a string.
    """
    show_id: constr(max_length=50)
    type: constr(max_length=50)
    title: constr(max_length=200)
    director: Optional[constr(max_length=300)] = ""
    cast: Optional[constr(max_length=1000)] = ""
    country: constr(max_length=200)
    date_added: date
    release_year: int
    rating: constr(max_length=20)
    duration: constr(max_length=20)
    listed_in: constr(max_length=500)
    description: Optional[constr(max_length=2000)] = ""
    class Config:
        orm_mode=True

class ShowSearch(BaseModel):
    show_id: Optional[constr(max_length=50)]=None
    type: Optional[constr(max_length=50)]=None
    title: Optional[constr(max_length=200)]=None
    director: Optional[constr(max_length=300)] = None
    cast: Optional[constr(max_length=1000)] = None
    country: Optional[constr(max_length=200)]=None
    date_added: Optional[date]=None
    release_year: Optional[int]=None
    rating: Optional[constr(max_length=20)]=None
    duration: Optional[constr(max_length=20)]=None
    listed_in: Optional[constr(max_length=500)]=None
    description: Optional[constr(max_length=2000)] = None
    class Config:
        orm_mode=True

class SearchSchema(BaseModel):
    """
    Search model with additional fields for simple pagination
    Parital Search is available on:
    title, director, cast, duration, listed_in, description
    If results are limited, but page number is not supplied, only the first page will be returned.
    """
    criteria:ShowSearch
    max_results:Optional[int]=None
    results_per_page:Optional[int]=None
    page_number:Optional[int]=1
    class Config:
        orm_mode=True
