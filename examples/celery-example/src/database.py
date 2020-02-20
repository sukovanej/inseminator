from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .configuration import Configuration


class Database:
    def __init__(self, configuration: Configuration) -> None:
        self.__engine = create_engine(configuration.connection_string)
        self.__session_maker = sessionmaker(self.__engine)

    def get_session(self) -> Session:
        return self.__session_maker()
