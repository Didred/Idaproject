import os
import io
import numpy
from io import BytesIO
import sqlalchemy
import requests
import base64
from PIL import Image
from resizeimage import resizeimage


from library.database import get_session
from library.model.picture import Picture


DEFAULT_CONFIG_DIRECTORY = os.getcwd()
DEFAULT_DATABASE_URL = ''.join(["sqlite:///",
                                DEFAULT_CONFIG_DIRECTORY,
                                "temp.db"])

class API:
    def __init__(self, connection_string):
        self._session = get_session(connection_string)

    def add(self, link, name, picture):
        if picture:
            image = Picture(name, picture)
        else:
            try:
                temp = requests.get(link)
                if temp.status_code == 200:
                    image = Picture(link, temp.content)
                else:
                    raise Exception
            except:
                raise Exception

        self._add(image)
        return image.id

    def get(self, picture_id):
        try:
            return (self._session.query(Picture)
                    .filter(Picture.id == picture_id).one_or_none())
        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Picture not found")

    def get_pictures(self):
        return self._session.query(Picture).all()

    def convert_picture(self, picture):
        return str(base64.b64encode(picture))[2: -1]

    def resize(self, id, new_width, new_height):
        image = self.get(id)
        picture = Image.open(io.BytesIO(image.picture))
        print(new_width, new_height)

        if not new_height:
            new_height = int((int(new_width) / image.width) * image.height)
        else:
            new_height = int(new_height)
        if not new_width:
            print(new_height / image.height)
            new_width = int((int(new_height) / image.height) * image.width)
        else:
            new_width = int(new_width)
        print(new_width, new_height)

        print(new_height, new_width)
        new_picture = picture.resize((new_width, new_height))
        buffered = BytesIO()
        new_picture.save(buffered, format="PNG")
        new_picture = base64.b64encode(buffered.getvalue())

        picture = Picture(image.name, new_picture, new_width, new_height)

        return picture

    def _add(self, object):
        self._session.add(object)
        self._session.commit()
