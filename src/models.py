from pydantic.dataclasses import dataclass
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.orm import relationship


from .database import Base

@dataclass
class Show(Base):
    """
    Representation of the Show table.
    """
    __tablename__ = "shows"

    id = Column(Integer,primary_key=True,index=True)
    show_id = Column(String,index=True)
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