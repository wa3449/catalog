#!/usr/bin/env python
#
# models.py
# The models.py module creates the model for the
# Item Catalog Project for Udacity Full Stack Nanodegree
#
# See README.md file for detailed information on the application
#
#
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy import DateTime


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    email = Column(String, nullable=False)
    picture = Column(String)
    password_hash = Column(String(64))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String)
    created_on = Column(DateTime())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_on': str(self.created_on),
            'category_id': self.category_id,
            'user_id': self.user_id
        }


engine = create_engine('sqlite:///instance/itemcatalog.db')


Base.metadata.create_all(engine)
