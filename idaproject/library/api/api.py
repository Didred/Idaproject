import os
import sqlalchemy
import requests


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


    def _add(self, object):
        self._session.add(object)
        self._session.commit()
