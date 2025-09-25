from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base


class Base:
    # Generate id automatically
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


Base = declarative_base(cls=Base)
