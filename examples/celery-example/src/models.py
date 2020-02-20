from typing import Any

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()


class Cow(Base):
    __tablename__ = "cow"

    id = Column(Integer, primary_key=True)
    pregnant = Column(Boolean)
    name = Column(String)
