from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.schema import CreateTable


engine = create_engine('sqlite:///taskmanager.db', echo = True)
sessionlocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

