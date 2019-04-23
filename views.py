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
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Category, Item, User
from datetime import datetime
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"


# Connect to Database and create database session


engine = create_engine('sqlite:///instance/itemcatalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


# methods for google and facebook login / disconnect

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


 #DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showHome'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showHome'))


# JSON api endpoints


@app.route('/catalog.JSON')
def getCatalogHandler():
    """ return all categories and category items """
    categories = getCategories()
    return jsonify(dict(Catalog=[dict(c.serialize,
            items=[i.serialize for i in c.items])
            for c in categories]))


@app.route('/catalog/<string:categoryName>/items/JSON')
def getItemsByCategoryHandler(categoryName):
    """ get items for a given category name """
    category = getCategoryByName(categoryName)
    if category:
        items = getItemsByCategoryId(category.id)
        if items:
            return jsonify(Item=[i.serialize for i in items])
        else:
            return jsonify(error="items not found"), 404
    else:
        return jsonify(error="category not found"), 404


@app.route('/catalog/<string:categoryName>/<string:itemName>/JSON')
def getItemByCategoryHandler(categoryName, itemName):
    """ get a specific category item by category and item name """
    item = getItemByCategory(categoryName, itemName)
    if item:
       return jsonify(Item = item.serialize)
    else:
        return jsonify(error="item not found"), 404


# view api routes


@app.route('/')
@app.route('/catalog')
def showHome():
    """ Shows a list of categories and the last 6
        items that have been added/updated """
    categories = getCategories()
    items = getLatestItems()
    categoryNames = list()
    if items:
        for i in items:
            category = getCategoryById(i.category_id)
            categoryNames.append(category.name)
    resultset = zip(items, categoryNames)    
    return render_template('home.html',
            categories=categories,
            resultset=resultset)


@app.route('/catalog/<string:category_name>/items')
def showItemsByCategory(category_name):
    categories = getCategories()
    category = getCategoryByName(category_name)
    items = getItemsByCategoryId(category.id)
    return render_template('categoryitems.html',
            categories=categories,
            category=category,
            items=items)


@app.route('/catalog/<string:category_name>/<string:item_name>')
def showItemDetail(category_name, item_name):
    category = getCategoryByName(category_name)
    item = getItemByCategory(category_name, item_name)
    return render_template('itemdetail.html',
            category=category,
            item=item)


@app.route('/catalog/add', methods=['GET', 'POST'])
def showAddItem():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'GET':
        categories = getCategories()
        return render_template('additem.html', categories=categories)
    elif request.method == 'POST':

        name = request.form['name']
        description = request.form['description']
        category = getCategoryByName(request.form['category'])
        category_id = category.id
        user_id = login_session['user_id']

        item = createItem(name, description, category_id, user_id)

        flash('"%s" add item was successful' % item.name)
        return redirect(url_for('showHome'))


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def showEditItem(item_name):

    if 'username' not in login_session:
        return redirect('/login')

    item = getItemByName(item_name)
    if item.user_id != login_session['user_id']:
        flash('user is not authorized to edit this item "%s"' % item.name)
        return redirect(url_for('showHome'))

    if request.method == 'GET':
        categories = getCategories()
        category = getCategoryById(item.category_id)
        return render_template('edititem.html',
                item=item,
                categoryName=category.name,
                categories=categories)
    elif request.method == 'POST':

        name = request.form['name']
        description = request.form['description']
        category = getCategoryByName(request.form['category'])
        category_id = category.id

        updateItem(item.id, name, description, category_id)

        flash('"%s" edit item was successful' % item.name)

        return redirect(url_for('showHome'))


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def showDeleteItem(item_name):

    if 'username' not in login_session:
        return redirect('/login')

    item = getItemByName(item_name)

    if item.user_id != login_session['user_id']:
        flash('user is not authorized to delete this item "%s"' % item.name)
        return redirect(url_for('showHome'))

    if request.method == 'GET':
        category = getCategoryById(item.category_id)
        return render_template('deleteitem.html', item=item, category=category)
    elif request.method == 'POST':

        if item:
            deleteItem(item.id)
            flash('"%s" delete item was successful' % item.name)
        else:
            flash('%s delete item was NOT successful' % item_name)
        return redirect(url_for('showHome'))


# api endpoints for seeding the database


@app.route('/catalog/user', methods=['POST'])
def userHandler():
    """ POST: add user """
    name = request.args.get('name')
    email = request.args.get('email')
    picture = request.args.get('picture')
    user = addUser(name, email, picture)
    return jsonify(User= user.serialize)


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
    newUser = User(username=login_session['username'],
                email=login_session['email'],
                picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def addUser(name, email, picture):
    user = User(username=name,
                email=email,
                picture=picture)
    session.add(user)
    session.commit()
    return user


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


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


def getCategoryByName(name):
    """ get a category by name """
    category = session.query(Category).filter_by(name = name).first()
    return category


def getCategoryById(id):
    """ get a category by id """
    category = session.query(Category).filter_by(id = id).first()
    return category


def createItem(name, description, category_id, user_id):
    """ Create an item """
    item = Item(name = name,
        description = description,
        edited_on = datetime.today(),
        category_id = category_id,
        user_id = user_id)
    if item:
        session.add(item)
        session.commit()
        return item
    return None


def getItemsByCategoryId(category_id):
    """ get items by category id """
    category = session.query(Category).filter_by(id = category_id).first()
    if category:
        items = session.query(Item).filter_by(category_id = category.id)
        return items
    return None


def getItemByCategory(categoryName, itemName):
    """ get item by a category name and item name """
    category = getCategoryByName(categoryName)
    if category:
        name = itemName.replace("+", " ")
        item = session.query(Item).\
            filter(Item.category_id == category.id).\
            filter(Item.name == name).first()
        return item
    return None


def getItemByName(itemName):
    """ Get item - if no item found, None is returned"""
    item = session.query(Item).filter_by(name = itemName).first()
    return item


def getLatestItems():
    items = session.query(Item).order_by(desc(Item.edited_on)).limit(5)
    return items



def updateItem(id, name, description, category_id):
    """ Update item """
    item = session.query(Item).filter_by(id = id).first()
    if item:
        item.name = name
        item.description = description
        item.category_id = category_id
        item.edited_on = datetime.today()
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
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
