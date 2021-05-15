import os

from typing import List

from fastapi import Depends,FastAPI,HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

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
    return "Hello CICD {}!".format(name)

@app.get("/shows/", response_model=List[schemas.ShowBase])
def show_records(db: Session = Depends(get_db)):
    shows = db.query(models.Show).all()
    return shows

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=int(os.environ.get("PORT", 8080)))