import os

from typing import List

from fastapi import Depends,FastAPI,HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session, relationship

import models,schemas
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
    name = os.environ.get("NAME", "World")
    return {"message":"Hello CICD {}!".format(name)}

@app.get("/showByRating/", response_model=List[schemas.SummaryCount])
def show_summary(db: Session = Depends(get_db)):
    summary = db.query(models.Show.rating,func.count(models.Show.rating)).all()
    return jsonable_encoder(summary)

@app.get("/shows/", response_model=List[schemas.ShowBase])
def show_records(db: Session = Depends(get_db)):
    shows = db.query(models.Show).all()
    return shows

@app.get("/show/{show_id}", response_model=schemas.ShowBase)
def get_show(show_id:str,db: Session= Depends(get_db)):
    return db.query(models.Show).filter(models.Show.show_id == show_id).first()

@app.post("/show/", response_model=schemas.ShowBase)
def create(s:schemas.ShowCreate, db: Session=Depends(get_db)):
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
    target = db.query(models.Show).filter(models.Show.id==id).first()
    db.delete(target)
    db.commit()
    return {"action" : f"{id} deleted"}

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=int(os.environ.get("PORT", 8080)))