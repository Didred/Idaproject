from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    BLOB
)

class Picture(Base):
    __tablename__ = 'picture'

    id = Column(Integer, primary_key=True)
    picture = Column(BLOB)
    height = Column(Integer)
    width = Column(Integer)

    def __init__(self, picture):
        self.picture = picture

