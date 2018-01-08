from sqlalchemy import Column, ForeignKey, Integer, String, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import yaml
import os

Base = declarative_base()


def db_connect(config='config.yaml'):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), config)
    with open(config_file, 'r') as f:
        db_conn_str = yaml.load(f.read())['database']
    return create_engine(db_conn_str)


class BaseCharacters(Base):
    __tablename__ = 'base_characters'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(250), nullable=False)
    secondary_name = Column(String(250), nullable=False)
    stars = Column(Integer, nullable=True)
    power1_color = Column(String(250), nullable=False)
    power1_cost = Column(Integer, nullable=True)
    power2_color = Column(String(250), nullable=False)
    power2_cost = Column(Integer, nullable=True)
    power3_color = Column(String(250), nullable=False)
    power3_cost = Column(Integer, nullable=True)


class RosterCharacters(Base):
    __tablename__ = 'roster_characters'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("base_characters.id"), nullable=False)
    level = Column(Integer, nullable=False)
    character_level_id = Column(String(250), nullable=False)
    power1_level = Column(Integer, nullable=False)
    power2_level = Column(Integer, nullable=False)
    power3_level = Column(Integer, nullable=False)


class CharacterStats(Base):
    __tablename__ = 'character_stats'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("base_characters.id"), nullable=False)
    character_level_id = Column(String(250), unique=True, nullable=False)
    level = Column(Integer, nullable=False)
    health = Column(Integer, nullable=False)
    yellow = Column(Integer, nullable=False)
    red = Column(Integer, nullable=False)
    blue = Column(Integer, nullable=False)
    purple = Column(Integer, nullable=False)
    green = Column(Integer, nullable=False)
    black = Column(Integer, nullable=False)
    critical = Column(DECIMAL, nullable=False)
    teamup = Column(Integer, nullable=False)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(Text, nullable=False)
    password_hash = Column(String(250))


def create_db():
    engine = db_connect()
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_db()
