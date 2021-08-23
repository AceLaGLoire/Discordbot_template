from typing import List
from sqlalchemy.orm.session import Session

from typing import TypeVar, Type

T = TypeVar("T")

# abstract
class BaseService:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def create(self, item) -> None:
        self.session.add(item)
        self.session.commit()

    def delete(self, items: List) -> None:
        [self.session.delete(item) for item in items]
        self.session.commit()

    def exists_by_guild(self, TYPE: Type[T], guild: int) -> bool:
        exists = self.session.query(
            self.session.query(TYPE).filter_by(guild=guild).exists()
        ).scalar()
        return exists

    def read_single(self, TYPE: Type[T], guild: int) -> T:
        return self.session.query(TYPE).filter_by(guild=guild).first()

    def read_multiple(self, TYPE: Type[T], guild: int) -> List[T]:
        return self.session.query(TYPE).filter_by(guild=guild).all()
