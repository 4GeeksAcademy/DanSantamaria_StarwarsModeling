import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(40), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    favorite_characters = relationship('FavoriteCharacter', back_populates='user')
    favorite_planets = relationship('FavoritePlanet', back_populates='user')


class Character(Base):
    __tablename__ = 'character'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(String(50), nullable=False)
    gender = Column(String(20), nullable=False)
    height = Column(String(20), nullable=False)
    mass = Column(String(20), nullable=False)
    eye_color = Column(String(50), nullable=False)
    hair_color = Column(String(50), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    favorites = relationship('FavoriteCharacter', back_populates='character')


class Planet(Base):
    __tablename__ = 'planet'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    climate = Column(String(100), nullable=False)
    terrain = Column(String(100), nullable=False)
    population = Column(String(100), nullable=False)
    diameter = Column(String(100), nullable=False)
    gravity = Column(String(50), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    favorites = relationship('FavoritePlanet', back_populates='planet')


class FavoriteCharacter(Base):
    __tablename__ = 'favorite_character'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    character_id = Column(Integer, ForeignKey('character.id'), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'character_id'),
    )
    
    user = relationship('User', back_populates='favorite_characters')
    character = relationship('Character', back_populates='favorites')


class FavoritePlanet(Base):
    __tablename__ = 'favorite_planet'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'planet_id'),
    )
    
    user = relationship('User', back_populates='favorite_planets')
    planet = relationship('Planet', back_populates='favorites')


render_er(Base, 'diagram.png')