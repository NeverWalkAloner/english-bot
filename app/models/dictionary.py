from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Dictionary(Base):
    __tablename__ = "dictionary"

    id = Column(Integer, primary_key=True, index=True)
    english = Column(String(100), index=True)
    russian = Column(String(2000))
