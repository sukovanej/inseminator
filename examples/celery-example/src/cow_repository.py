from typing import List

from .database import Database
from .models import Cow


class CowRepository:
    def __init__(self, database: Database):
        self.__session = database.get_session()

    def get_not_pregnant_cows(self, limit: int) -> List[Cow]:
        return self.__session.query(Cow).filter(Cow.pregnant == False).limit(limit).all()

    def inseminate_cow(self, cow: Cow) -> None:
        cow.pregnant = True
        self.__session.flush()

    def add_cow(self, name: str) -> Cow:
        cow = Cow(name=name, pregnant=False)
        self.__session.add(cow)
        return cow

    def commit(self) -> None:
        self.__session.commit()
