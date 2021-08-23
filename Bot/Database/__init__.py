import os

from sqlalchemy.engine.base import Engine

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import base

connectionString = ""
if os.getenv("DATABASE"):
    connectionString = os.getenv("DATABASE")
else:
    protocol = os.getenv("DB_PROTOCOL")
    location = os.getenv("DB_LOCATION")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database_name = os.getenv("DB_DATABASE")
    connectionString = f"{protocol}://{user}:{password}@{location}/{database_name}"

Base: base = declarative_base()


# 'postgresql://postgres:password@localhost/database'

engine: Engine = create_engine(connectionString)

from Bot.Models.Settings import Settings

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
