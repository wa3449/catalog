from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User
from datetime import datetime


engine = create_engine('sqlite:///instance/itemcatalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

# api endpoints


@app.route('/categories', methods=['GET', 'POST'])
def categories_handler():
    if request.method == 'GET':
        categories = getAllCategories()
        result = jsonify(Category=[i.serialize for i in categories])
        return result
    elif request.method == 'POST':
        name = request.args.get('name')
        if name:
            category = createCategory(name)
            if category:
                return jsonify(Category = category.serialize)
            else:
                return jsonify(error="create Category failed")
        else:
            return jsonify(error="not enough info to create a category")



@app.route('/categories/<int:id>', methods=['GET'])
def category_handler(id):
    if request.method == "GET":
        category = getCategory(id)
        return jsonify(Category = category.serialize)
    else:
        return jsonify(error="category not found")


@app.route('/items', methods=['GET', 'POST'])
def items_handler():
    if request.method == 'GET':
        items = getAllItems()
        result = jsonify(Item=[i.serialize for i in items])
        return result
    elif request.method == 'POST':
        name = request.args.get('name')
        description = request.args.get('description')
        category_id = request.args.get('category')
        user_id = request.args.get('user')
        if name:
            item = createItem(name, description, category_id, user_id)
            if item:
                return jsonify(Item = item.serialize)
            else:
                return jsonify(error="create item failed")
        else:
            return jsonify(error="not enough info to create an item")


# model methods


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
    item = Item(name = name,
        description = description,
        created_on = datetime.today(),
        category_id = category_id,
        user_id = user_id)
    if item:
        session.add(item)
        session.commit()
        return item
    return None


def getAllItems():
    """ Get all items - if no item(s) found, None is returned """
    items = session.query(Item).all()
    return items


def getAllItemsForACategory(category_id):
    """ Get all items for a category - if no item(s) found, None is returned """
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
    app.run(host='0.0.0.0', port=5000)
