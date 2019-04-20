#!/usr/bin/env python
#
# seedb.py
# This module contains:
#    API calls to load the database
#    Simple test for the JSON API endpoints for the
# Item Catalog Project for Udacity Full Stack Nanodegree
#
# See README.md file for detailed information on the application
#
#
import httplib2
import sys
import json

address = 'http://localhost:5000'

# Step 1: load categories - writing genres

print "load categories"

try:

    url = address + '/catalog/categories?name=Fantasy'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/catalog/categories?name=Science+Fiction'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/catalog/categories?name=Westerns'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/catalog/categories?name=Romance'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/catalog/categories?name=Thriller'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/catalog/categories?name=Mystery'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/catalog/categories?name=Detective+Story'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/catalog/categories?name=Dystopia'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

except Exception as err:
	print "Step 1 FAILED: Could not add new categories"
	print err.args
	sys.exit()
else:
	print "Step 1 PASS: Succesfully made all new categories"

# Step 2: load items - Novels

try:

# Fantasy

    description = "It tells of a young girl named Alice falling through a rabbit hole into a fantasy world populated by peculiar, anthropomorphic creatures."
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=Alice+in+Wonderland&description=%s&category=1&user=1" % urldescription

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


    description = "The Chronicles of Narnia is a series of seven fantasy novels by C. S. Lewis."
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=The+Chronicles+of+Narnia&description=%s&category=1&user=1" % urldescription

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


    description = "Charlie and the Chocolate Factory is a 1964 children's novel by British author Roald Dahl. The story features the adventures of young Charlie Bucket inside the chocolate factory of eccentric chocolatier Willy Wonka."
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=Charlie+and+the+Chocolate+Factory&description=%s&category=1&user=1" % urldescription

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


    description = "Harry Potter is a series of fantasy novels written by British author J. K. Rowling. The novels chronicle the lives of a young wizard, Harry Potter, and his friends Hermione Granger and Ron Weasley, all of whom are students at Hogwarts School of Witchcraft and Wizardry. The main story arc concerns Harry's struggle against Lord Voldemort, a dark wizard who intends to become immortal, overthrow the wizard governing body known as the Ministry of Magic, and subjugate all wizards and Muggles (non-magical people)."
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=Harry+Potter&description=%s&category=1&user=1" % urldescription

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


    description = "The Hobbit, or There and Back Again is a children's fantasy novel by English author J. R. R. Tolkien. The Hobbit is set within Tolkien's fictional universe and follows the quest of home-loving hobbit Bilbo Baggins to win a share of the treasure guarded by Smaug the dragon. Bilbo's journey takes him from light-hearted, rural surroundings into more sinister territory."
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=The+Hobbit&description=%s&category=1&user=1" % urldescription

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

# Science fiction

    description = "The War of the Worlds is a science fiction novel by English author H. G. Wells. The novel is the first-person narrative of both an unnamed protagonist in Surrey and of his younger brother in London as southern England is invaded by Martians."
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=The+War+of+the+Worlds&description=%s&category=2&user=1" % urldescription

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


    description = "Journey to the Center of the Earth is an 1864 science fiction novel by Jules Verne. The story involves German professor Otto Lidenbrock who believes there are volcanic tubes going toward the centre of the Earth."
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=Journey+to+the+Center+of+the+Earth&description=%s&category=2&user=1" % urldescription
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


    description = "The Lost Planet is a 1953 juvenile science fiction novel by Angus MacVicar, published by Burke, London. It is the first of the popular novel series The Lost Planet, which was adapted for radio and television."
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=The+Lost+Planet&description=%s&category=2&user=1" % urldescription

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

# Mystery

    description = '"The Adventure of Silver Blaze", one of the 56 Sherlock Holmes short stories written by Sir Arthur Conan Doyle. One of the most popular Sherlock Holmes short stories, "Silver Blaze" focuses on the disappearance of the eponymous race horse (a famous winner) on the eve of an important race and on the apparent murder of its trainer.'
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=The+Adventure+of+Silver+Blaze&description=%s&category=6&user=1" % urldescription

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


    description = "The Mysterious Affair at Styles is a detective novel by British writer Agatha Christie. Styles was Christie's first published novel. It introduced Hercule Poirot, Inspector Japp, and Arthur Hastings. Poirot, a Belgian refugee of the Great War, is settling in England near the home of Emily Inglethorp, who helped him to his new life. His friend Hastings arrives as a guest at her home. When the woman is killed, Poirot uses his detective skills to solve the mystery."
    urldescription = description.replace(' ', '+')

    url = address + "/catalog/items?name=The+Mysterious+Affair+at+Styles&description=%s&category=6&user=1" % urldescription

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


except Exception as err:
	print "Step 2 FAILED: Could not add new items"
	print err.args
	sys.exit()
else:
	print "Step 2 PASS: Succesfully Made all new items"

# Test 1 - JSON api endpoint tests

try:
    # get catalog
    url = address + "/catalog.JSON"

    h = httplib2.Http()
    resp, result = h.request(url, 'GET')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


    # get all items for a category
    category = "Fantasy"
    url = address + "/catalog/%s/items/JSON" % category

    h = httplib2.Http()
    resp, result = h.request(url, 'GET')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


    # get a specific category item by category and item name
    category = "Fantasy"
    item = "Alice+in+Wonderland"
    url = address + "/catalog/{category}/{item}/JSON".format(category=category, item=item)

    h = httplib2.Http()
    resp, result = h.request(url, 'GET')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)


except Exception as err:
	print "Test 1 FAILED:  could not successfully execute JSON API endpoints"
	print err.args
	sys.exit()
else:
	print "Test 1 PASS: Succesfully passed all tests"
