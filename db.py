from sqlalchemy import Column, Integer, String, select, update
from sqlalchemy.orm import declarative_base, declared_attr

from config import DEFAULT_GROUP


class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class DB:
    engine = None
    session = None


class UserGroup(Base):
    telegram_id = Column(Integer, unique=True)
    group_name = Column(String(6))

    def __repr__(self):
        return f'User {self.telegram_id} {self.group_name}'


def save_group(telegram_id, group_name):
    result = DB.session.execute(
        select(UserGroup).where(UserGroup.telegram_id == telegram_id)
    ).first()
    if result:
        DB.session.execute(
            update(UserGroup).where(
                UserGroup.telegram_id == telegram_id
            ).values(group_name=group_name)
        )
    else:
        DB.session.add(
            UserGroup(
                telegram_id=telegram_id,
                group_name=group_name,
            )
        )
    DB.session.commit()


def get_group(telegram_id):
    result = DB.session.query(UserGroup).filter(
        UserGroup.telegram_id == telegram_id
    ).first()
    if result:
        return result.group_name
    return DEFAULT_GROUP
