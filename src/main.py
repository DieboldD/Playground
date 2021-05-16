import os

from typing import List

from fastapi import Depends,FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, extract
from sqlalchemy.sql import label
from sqlalchemy.orm import Session


import models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def hello_world():
    """
    Typical Hello World.
    """
    name = os.environ.get("NAME", "World")
    return {"message":"Hello CICD {}!".format(name)}

@app.get("/showAggregation/")
def show_summary(db: Session = Depends(get_db)):
    """
    Show Aggregation, via SQLAlchemy query
    """
    baseQuery = db.query(models.Show.rating,
                            label('year_added',extract('year',models.Show.date_added)),
                            label('total',func.count())
                            ).group_by(models.Show.rating,extract('year',models.Show.date_added))
    ratingAggregation = baseQuery.all()
    last5Years = baseQuery.filter(extract('year',models.Show.date_added) <= 2021).all()
    aggregation =  {
                     "ShowsAddedByRatingByYear":ratingAggregation,
                     "WithinTheLast5Years":last5Years
                   }
    return jsonable_encoder(aggregation)

@app.get("/shows/", response_model=List[schemas.ShowBase])
def show_records(db: Session = Depends(get_db)):
    """
    Raw Get Records
    """
    shows = db.query(models.Show).all()
    return shows

@app.post("/shows/search/")
def search_shows(searchSchema:schemas.SearchSchema,db:Session=Depends(get_db)):
    """
    Search by data:
    If a field is not none, then it is considered.
    If results are limited, but page number is not supplied, only the first page will be returned.
    """
    s=searchSchema.criteria
    baseQuery = db.query(models.Show)

    if s.show_id is not None:
        baseQuery= baseQuery.filter_by(models.Show.show_id == s.show_id)
    if s.type is not None:
        baseQuery= baseQuery.filter_by(models.Show.type == s.type)
    if s.title is not None:
        baseQuery= baseQuery.filter_by(s.title in models.Show.title)
    if s.director is not None:
        baseQuery= baseQuery.filter_by(s.director in models.Show.director)
    if s.cast is not None:
        baseQuery= baseQuery.filter_by(s.cast in models.Show.cast)
    if s.country is not None:
        baseQuery= baseQuery.filter_by(models.Show.country == s.country)
    if s.date_added is not None:
        baseQuery= baseQuery.filter_by(models.Show.date_added == s.date_added)
    if s.release_year is not None:
        baseQuery= baseQuery.filter_by(models.Show.release_year == s.release_year)
    if s.rating is not None:
        baseQuery= baseQuery.filter_by(models.Show.rating == s.rating)
    if s.duration is not None:
        baseQuery= baseQuery.filter_by(s.duration in models.Show.duration)
    if s.listed_in is not None:
        baseQuery= baseQuery.filter_by(s.listed_in in models.Show.listed_in)
    if s.description is not None:
        baseQuery= baseQuery.filter_by(s.description in models.Show.description)

    if searchSchema.max_results is not None:
        baseQuery=baseQuery.limit(searchSchema.max_results)
    
    if searchSchema.results_per_page is not None:
        baseQuery=baseQuery.slice(searchSchema.page_number*searchSchema.results_per_page,searchSchema.page_number*searchSchema.results_per_page+searchSchema.results_per_page)

    result = baseQuery.all()
    return result
            
@app.get("/show/{id}", response_model=schemas.ShowBase)
def get_show(id:int,db: Session= Depends(get_db)):
    """
    Get Show by primary key
    """
    return db.query(models.Show).filter(models.Show.id == id).first()

@app.post("/show/", response_model=schemas.ShowBase)
def create(s:schemas.ShowCreate, db: Session=Depends(get_db)):
    """
    Create Show
    """
    target = models.Show(show_id= s.show_id,
        type = s.type,
        title = s.title,
        director = s.director,
        cast = s.cast,
        country = s.country,
        date_added = s.date_added,
        release_year = s.release_year,
        rating = s.rating,
        duration = s.duration,
        listed_in = s.listed_in,
        description = s.description
    )
    db.add(target)
    db.commit()
    db.refresh(target)
    return target

@app.put("/show/{id}", response_model=schemas.ShowBase)
def update(id:int, s:schemas.ShowCreate, db: Session=Depends(get_db)):
    """
    Update existing show.
    """
    target = db.query(models.Show).filter(models.Show.id==id).first()
    target.show_id= s.show_id
    target.type = s.type
    target.title = s.title
    target.director = s.director
    target.cast = s.cast
    target.country = s.country
    target.date_added = s.date_added
    target.release_year = s.release_year
    target.rating = s.rating
    target.duration = s.duration
    target.listed_in = s.listed_in
    target.description = s.description
    db.commit()
    db.refresh(target)
    return target


@app.delete("/show/{id}")
def delete(id:int, db: Session=Depends(get_db)):
    """
    Delete show by primary key.
    """
    target = db.query(models.Show).filter(models.Show.id==id).first()
    db.delete(target)
    db.commit()
    return {"action" : f"{id} deleted"}

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=int(os.environ.get("PORT", 8080)))