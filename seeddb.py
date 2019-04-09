import httplib2
import sys
import json

address = 'http://localhost:5000'

# Load categories - writing genres

print "Test 1: creating categories"

try:

    url = address + '/categories?name=Fantasy'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/categories?name=Science+Fiction'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/categories?name=Westerns'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/categories?name=Romance'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/categories?name=Thriller'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/categories?name=Mystery'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/categories?name=Detective+Story'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

    url = address + '/categories?name=Dystopia'
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

except Exception as err:
	print "Test 1 FAILED: Could not add new categories"
	print err.args
	sys.exit()
else:
	print "Test 1 PASS: Succesfully Made all new categories"

# Test 2 - add items - Novels

try:

    url = address + "/items?name=Alice+in+Wonderland&description=It+tells+of+a+young+girl+named+Alice+falling+through+a+rabbit+hole+into+a+fantasy+world+populated+by+peculiar,+anthropomorphic+creatures.&category=3&user=1"
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    print json.loads(result)

except Exception as err:
	print "Test 2 FAILED: Could not add new items"
	print err.args
	sys.exit()
else:
	print "Test 1 PASS: Succesfully Made all new items"
