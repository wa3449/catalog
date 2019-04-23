# Project Description
The Item Catalog Tool is a python application that manages a list of items within a set of pre-defined categories.
The contents of the item catalog can be viewed by anyone using a browser based GUI or a set of REST APIs.
Registered users who authenticate with their Google or Facebook login information can add items, and update and delete items that they have previously added via the GUI.
All GUI views will display a Login/Logout control which can be used to login or to logout of the Item Catalog Tool GUI.
The context for this item catalog implementation is Literary Genres.

The item catalog tool GUI supports the following views:
1. Home - the Home view displays a list of categories in one pane, and a list of 5 items that were most recently added/updated. The Home view will display an Add Item control for registered users.
2. Category Items - the Category Items view displays all the items for a selected category.
3. Item Detail - the Item Detail view displays item details.
4. Add Item - the Add Item view supports a form that can be used to add an item.
4. Edit Item - the Edit Item view supports a form that can be used to update item attributes and category relationship.
5. Delete Item - the Delete Item view supports a form that can be used to delete an item.
6. Login - the login view displays a means to support user login via Google or Facebook.

The item catalog tool REST APIs support the following operations:
1. Get all categories and for each category, all category items.
2. Get all categories.
3. Get all items for a category.

There are also API endpoints which are used to seed the item catalog database:
1. Create a user.
2. Create a category.
3. Create a category item.

The model:

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

## Requirements
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

### Install and configure the VM
A Linux-based virtual machine (VM) is used to run an SQL database server and python
application on your computer. This project is using tools called Vagrant
and VirtualBox to install and manage the VM. Use the following URLs to install Vagrant and VirtualBox. (Note: an older version of VirtualBox is used for this project.)

* [Virtual Box 5.1](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* [Vagrant](https://www.vagrantup.com)

Use this [Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile) to ensure the VM is configured properly. The Vagrantfile should be stored in the vagrant directory.

In the vagrant directory, type **vagrant up** to launch your virtual machine.

Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt.
Change directory to the /vagrant directory by typing **cd /vagrant**.

### Get the item catalog project from Github

Clone the remote git repo for the log analysis project on your computer using the web URL:

```
https://github.com/wa3449/log_analysis_project.git
```
### Create the database schema and load the data needed for the Project

You will need to open 2 terminal windows running the vagrant shell.
The VM should be up and running from 1 of the terminal windows.

1. Create the database instance: (from the application root directory: /vagrant/catalog)

```
$ python models.py
```

2. Seed the database: (from the application root directory: /vagrant/catalog)

```
$ python views.py
```

The python application that seeds the item catalog database is dependent on an active views.py application.
```
$ python seeddb.py
```

## Usage
The python application will run from the command line and does not require
any input from the user. The python application connects to the item catalog database
and waits to process incoming http requests.

1. From the Item Catalog Tool project directory, run the application by typing the following command on the command line:

```
$ python views.py
```

2. Open a browser and type the following to display the Item Catalog Tool home view:

```
http://localhost:5000
```
