#!/usr/bin/env python
#
# views.py
# This module contains:
#    JSON API endpoints
#    view API endpoints
#    model methods for the
# Item Catalog Project for Udacity Full Stack Nanodegree
#
# See README.md file for detailed information on the application
#
#
from flask import Flask, request, jsonify
from flask import render_template, redirect, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Category, Item, User
from datetime import datetime


engine = create_engine('sqlite:///instance/itemcatalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)


# JSON api endpoints 


@app.route('/catalog.JSON', methods=['GET'])
def getCatalogHandler():
    """ return all categories and category items """
    categories = getCategories()
    return jsonify(dict(Catalog=[dict(c.serialize, items=[i.serialize
                                                     for i in c.items])
                         for c in categories]))


@app.route('/catalog/<string:categoryName>/items/JSON', methods=['GET'])
def getItemsByCategoryHandler(categoryName):
    """ get items for a given category name """
    category = getCategory(categoryName)
    if category:
        items = getItemsByCategory(category.id)
        if items:
            return jsonify(Item=[i.serialize for i in items])
        else:
            return jsonify(error="items not found"), 404
    else:
        return jsonify(error="category not found"), 404


@app.route('/catalog/<string:categoryName>/<string:itemName>/JSON', methods=['GET'])
def getItemByCategoryHandler(categoryName, itemName):
    """ get a specific category item by category and item name """
    item = getItemByCategory(categoryName, itemName)
    if item:
       return jsonify(Item = item.serialize)
    else:
        return jsonify(error="item not found"), 404


# view api routes

@app.route('/catalog/<string:itemName>/edit', methods=['GET', 'POST'])
def editItemHandler(itemName):
    """ """
#   if 'username' not in login_session:
#       return redirect('/login')

    item = getItem(itemName)

#   if item.user_id != login_session['user_id']:
#       return

    if request.method == 'GET':
#       return render_template('edititem.html', item=item)
        return jsonify(Item = item.serialize)
    elif request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        categoryName = request.form['category']

        category = getCategory(categoryName)

        updateItem(item.id, name, description, category_id)
#       flash('%s item edited' % item.name)
#       return redirect(url_for('xyz'))     
        return jsonify(Item = item.serialize)

        
@app.route('/catalog/<string:itemName>/delete', methods=['GET', 'POST'])
def deleteItemHandler(itemName):
    """ """
#   if 'username' not in login_session:
#       return redirect('/login')


    item = getItem(itemName)

#   if item.user_id != login_session['user_id']:
#       return

    if request.method == 'GET':
#       return render_template('deleteitem.html', item=item)
        return jsonify(Item = item.serialize)
    elif request.method == 'POST':
        deleteItem(item.id)
#       flash('%s item edited' % item.name)
#       return redirect(url_for('xyz'))     
        return jsonify(Item = item.serialize)

# api endpoints for seeding the database


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


def getCatalog():
    """ join category and items """
    categories = session.query(Category).options(joinedload(Category.items)).all()
    return categories


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
    category = session.query(Category).filter_by(id = category_id).first()
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


def getItem(itemName):
    """ Get item - if no item found, None is returned"""
    item = session.query(Item).filter_by(name = itemName).first()
    return item


def updateItem(id, name, description, category_id):
    """ Update item """
    item = session.query(Item).filter_by(id = id).first()
    if item:
        if not name:
            item.name = name
        if not description:
            item.description = description
        if not category_id:
            item.category_id = category_id
        session.add(item)
        session.commit()
    return None


def deleteItem(item_id):
    """ Delete item """
    item = session.query(Item).filter_by(id = item_id).first()
    if item:
        session.delete(item)
        session.commit()
    return None


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
