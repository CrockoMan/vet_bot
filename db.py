from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, declared_attr


class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class Who_Where(Base):
    number = Column(Integer, unique=True)
    title = Column(String(6))

    def __repr__(self):
        return f'PEP {self.number} {self.title}'
