from pydantic.dataclasses import dataclass
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.orm import relationship


from src.database import Base

@dataclass
class Show(Base):
    __tablename__ = "shows"

    show_id = Column(String,primary_key=True,index=True)
    type = Column(String)
    title = Column(String)
    director = Column(String)
    cast = Column(String)
    country = Column(String)
    date_added = Column(Date)
    release_year = Column(Integer)
    rating = Column(String)
    duration = Column(String)
    listed_in = Column(String)
    description = Column(String)