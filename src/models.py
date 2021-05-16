from pydantic.dataclasses import dataclass
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.orm import relationship


from src.database import Base

@dataclass
class Show(Base):
    """
    Representation of the Show table.
    """
    __tablename__ = "shows"

    id = Column(Integer,primary_key=True,index=True)
    show_id = Column(String(50),index=True)
    type = Column(String(50))
    title = Column(String(200))
    director = Column(String(300))
    cast = Column(String(1000))
    country = Column(String(200))
    date_added = Column(Date)
    release_year = Column(Integer)
    rating = Column(String(20))
    duration = Column(String(20))
    listed_in = Column(String(500))
    description = Column(String(2000))