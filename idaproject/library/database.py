from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
)

Base = declarative_base()


def get_session(connection_string):
    engine = create_engine(connection_string, connect_args={'check_same_thread': False})
    session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return scoped_session(session)
