from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    BLOB
)
from PIL import Image
import io

class Picture(Base):
    __tablename__ = 'picture'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    picture = Column(BLOB)
    height = Column(Integer)
    width = Column(Integer)

    def __init__(self, name, picture, width=None, height=None):
        self.name = name
        self.picture = picture
        if width:
            self.width = width
            self.height = height
        else:
            self.width, self.height = Image.open(io.BytesIO(picture)).size

