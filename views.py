from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User


engine = create_engine('sqlite:///instance/itemcatalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)


def createCategory(name):
    """ Create new category """
    category = Category(name = name)
    if category:
        session.add(category)
        session.commit()
        return category
    else:
        return None


def getAllCategories():
    """ Get all categories - if no categories found, None is returned """
    categories = session.query(Category).all()
    return categories


def getCategory(id):
    """ Get a single category - if no category found, None is returned """
    category = session.query(Category).filter_by(id = id).one_or_none()
    return category
    

def createItem(name, description, category_id, user_id):
    """ Create an item """
    item = Item(name = name, description = description, category_id = category_id, user_id = user_id)
    if item:
        session.add(item)
        session.commit()
        return item
    return None

def getAllItemsForACategory(category_id):
    """ Get all items for a category - if not item(s) found, None is returned """
    category = session.query(Category).filter_by(id = category_id).one_or_none()
    if category:
        items = session.query(Item).filter_by(category_id = category.id)
        return items
    return None


def getItem(id):
    """ Get item - if no item found, None is returned"""
    item = session.query(Item).filter_by(id = id).one_or_none()
    return item


def updateItem(id, name, description, user_id):
    """ Update item """
    item = session.query(Item).filter_by(id = id).one_or_none()
    if item:
        if item.user_id != user_id:
            return 401
        if not name:
            item.name = name
        if not description:
            item.description = description

        session.add(item)
        session.commit()
        return 200
    else:
        return 404


def deleteItem(item_id, user_id):
    """ Delete item """
    item = session.query(Item).filter_by(id = item_id).one_or_none()
    if item:
        if item.user_id != user_id:
            return 401

        session.delete(item)
        session.commit()
        return 200
    else:
        return 404


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
