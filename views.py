from flask import Flask, request, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Category, Item, User


engine = create_engine('sqlite:///instance/itemcatalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

# api endpoints 

@app.route('/catalog/<string:categoryName>/items', methods=['GET'])
def getItemsByCategoryHandler(categoryName):
    """ get items for a given category """
    category = getCategory(categoryName)
    if category:
        items = getItemsByCategory(category.id)
        if items:
            return jsonify(Item=[i.serialize for i in items])
        else:
            return jsonify(error="items not found")
    else:
        return jsonify(error="category not found")


@app.route('/catalog/<string:categoryName>/<string:itemName>', methods=['GET'])
def getItemByCategoryHandler(categoryName, itemName):
    item = getItemByCategory(categoryName, itemName)
    if item:
        return jsonify(Item = item.serialize)
    else:
        return jsonify(error="item not found")


# api endpoints for seeding the db load

@app.route('/catalog/categories', methods=['GET', 'POST'])
def categoriesHandler():
    """ GET: get all categories and POST: create category """
    if request.method == 'GET':
        categories = getCategories()
        return jsonify(Category=[i.serialize for i in categories])
    elif request.method == 'POST':
        name = request.args.get('name')
        if name:
            category = createCategory(name)
            if category:
                return jsonify(Category = category.serialize)
            else:
                return jsonify(error="create Category failed")
        else:
            return jsonify(error="insufficient data to create a category")


@app.route('/catalog/items', methods=['POST'])
def itemsHandler():
    """ POST: create item """
    if request.method == 'POST':
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
            return jsonify(error="insufficient data to create an item")


# model methods for user, category, and item


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
        user = session.query(User).filter_by(email=email).one_or_none()
        return user


def createCategory(name):
    """ Create new category """
    category = Category(name = name)
    if category:
        session.add(category)
        session.commit()
        return category
    else:
        return None


def getCategories():
    """ get categories """
    categories = session.query(Category).all()
    return categories


def getCategory(name):
    """ get a category by name """
    category = session.query(Category).filter_by(name = name).first()
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


def getItemsByCategory(category_id):
    """ get items by category id """
    category = session.query(Category).filter_by(id = category_id).one_or_none()
    if category:
        items = session.query(Item).filter_by(category_id = category.id)
        return items
    return None


def getItemByCategory(categoryName, itemName):
    """ get item by a category name and item name """
    category = getCategory(categoryName)
    if category:
        name = itemName.replace("+", " ")
        item = session.query(Item).\
            filter(Item.category_id == category.id).\
            filter(Item.name == name).first()
        return item
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
