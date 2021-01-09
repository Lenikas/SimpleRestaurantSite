from contextlib import contextmanager
from decimal import Decimal
from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine('sqlite:///bd.sqlite')
Session = sessionmaker(bind=engine)
Base: Any = declarative_base()


@contextmanager
def create_session(**kwargs: Any) -> Any:
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


class UserReserve(Base):
    __tablename__ = 'user_reserve'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.String(100), nullable=False)
    phone = sa.Column(sa.String(100), nullable=False)
    mail = sa.Column(sa.String(100))
    date = sa.Column(sa.String, nullable=False)
    table_number = sa.Column(sa.Integer, nullable=False)

    def __init__(self, name: str, phone: str, mail: str, date: sa.Date, table_number: int):
        self.name = name
        self.phone = phone
        self.mail = mail
        self.date = date
        self.table_number = table_number


Base.metadata.create_all(engine)
