# Name
Item Catalog Tool
# Project Description
The Item Catalog Tool is a python application that manages a list of items within a set of pre-defined categories.
Registered users who have successfully authenticated with their Google or Facebook login will have the ability to post, edit and delete their own items.
The solution space for this particular implementation of category/item(s) is Literary Genres.
Literary Genres include works of prose, poetry, drama, hybrid forms, or other literature that are distinguished by
shared literary conventions, similarities in topic, theme, style, or common
settings, character types, or formulaic patterns of character interactions
and events, and an overall predictable form

The Item Catalog Tool has a browser based GUI and a number of API endpoints that provide access to the item catalog data.

## The GUI and HTML endpoints
The item catalog tool GUI supports the following views:
1. Home - the Home view displays a list of categories in one pane, and a list of 5 items that were most recently added/updated. The Home view will display an Add Item control for a user that has logged in. The following URLs are examples of supported endpoints:
* "address/"
* "address/catalog"
2. Category Items - the Category Items view displays all the items for a selected category. The following URL is an example of the category items endpoint:
* "address/catalog/<string:categoryName>/items"
3. Item Detail - the Item Detail view displays item details. The following URL is an example of the category items endpoint:
* "address/catalog/<string:categoryName>/<string:itemName>"
4. Add Item - the Add Item view supports a form that can be used to add an item. The following URL is an example of the category items endpoint:
* "address/catalog/add"
5. Edit Item - the Edit Item view supports a form that can be used to update item attributes and category relationship. The following URL is an example of the category items endpoint:
* "address/catalog/<string:itemName>/edit"
6. Delete Item - the Delete Item view supports a form that can be used to delete an item. The following URL is an example of the category items endpoint:
* "address/catalog/<string:itemName>/delete"
7. Login - the login view displays a means to support user login via Google or Facebook.

## REST API Endpoints
The item catalog tool REST APIs support the following operations:
1. Get all categories and for each category, all category items: "address/catalog.JSON"
2. Get all items for a category: "address/catalog/<string:categoryName>/items/JSON"
3. Get all a specific item for a category: "address/catalog/<string:categoryName>/<string:itemName>/JSON"

## REST API Endpoints for database seeding
There are also API endpoints which are used to seed the item catalog database:
1. Create a user: "address/catalog/user"
2. Create a category "address/catalog/categories"
3. Create a category item: "address/catalog/items"

## The model:

The model consists of 3 object types:
1. category
2. item
3. user

Each of the object types has the following data elements:
1. category
- id, pk
- name, string, indexed
2. item
- id, pk
- name, string, indexed
- description, string
- edited_on, datetime
- category id, fk
- user id, fk
3. user
- id, integer, pk
- username, string, indexed
- email, string, indexed
- password_hash, string
- picture, string

The object types have the following relationships:
1. category, 1:M item
2. user , 1:M item

The application supports the following operations on the object types:
1. categories - cr
2. item - crud
3. user - cr

The object types must support the following regulations:
1. An item can only be updated or deleted by the user that created the item
2. Only an authenticated and authorized user can add, update, or delete an item

# Requirements

## Structure
The Item Catalog Tool uses the following enabling technologies:

The application uses the following tools:
1. Environment
- VirtualBox
- Vagrant
2. Database
- sqlite
- SQLAlchemy
3. Presentation
- HTML
- CSS
4. Program
- Python
- Flask

To run the Item Catalog Tool on your local computer, you will need the
following:

## Install and configure the VM
A Linux-based virtual machine (VM) is used to run an SQL database server and python
application on your computer. This project is using tools called Vagrant
and VirtualBox to install and manage the VM. Use the following URLs to install Vagrant and VirtualBox. (Note: an older version of VirtualBox is used for this project.)

* [Virtual Box 5.1](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* [Vagrant](https://www.vagrantup.com)

Use this [Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile) to ensure the VM is configured properly. The Vagrantfile should be stored in the vagrant directory.

In the vagrant directory, type **vagrant up** to launch your virtual machine.

Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt.
Change directory to the /vagrant directory by typing **cd /vagrant**.

## Get the item catalog project from Github

Clone the remote git repo for the log analysis project on your computer using the web URL:

```
https://github.com/wa3449/catalog.git
```

## Application directory structure

The application directory is /Catalog with the following sub-directories:

```
/catalog
    /instance
    /static
    /templates
```

1. The catalog directory is the application directory
2. The instance directory contains the Item Catalog Tool database instance
3. The static directory contains reference files used by the presentation
4. The templates directory contains the application HTML files

## Application Code

1. models.py - Creates the database instance
2. seeddb.py - Seeds the database instance. Note: there is a dependency on running the views.py since API endpoints are used by seeddb.py to seed the database. I did this to get more experience with API endpoints and JSON but would change this in the future to remove the dependency with the application.py code.
3. application.py - Supports the HTML, JSON, and other endpoints for the application, model methods, and main loop.

## Create the database schema and load the data needed for the Project

You will need to open 2 terminal windows running the vagrant shell.
The VM should be up and running from 1 of the terminal windows.

1. Create the database instance. Execute the following command from the application root directory.

```
$ python models.py
```

2. Seed the database.
application.py must be running for the successful execution of seeddb.py application.
The seeddb.py application uses RESTful APIs supported by application.py to seed the database.

```
$ python application.py
```

The python application that seeds the item catalog database is dependent on an active application.py application.
```
$ python seeddb.py
```

## Usage
The python application will run from the command line.
The python application connects to the item catalog database and waits to process incoming http requests.
The GUI can be used to add/update/delete items for a Registered user.
Another application or curl request can be used to access the REST APIs.

1. From the Item Catalog Tool project directory, run the application by typing the following command on the command line:

```
$ python application.py
```

2. Open a browser and type the following to display the Item Catalog Tool GUI:

```
http://localhost:5000
```
