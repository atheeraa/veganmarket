from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Department, Item
from flask import send_from_directory
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Vegan Market"


app = Flask(__name__)
engine = create_engine('sqlite:///veganmarket.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
     
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


# JSON APIs to view a department Information
@app.route('/departments/<int:department>/items/JSON')
def departmentJSON(department_id):
    department = session.query(Department).filter_by(id=department_id).one()
    items = session.query(Item).filter_by(
        department_id=department_id).all()
    return jsonify(Item=[i.serialize for i in items])

#JSON for item
@app.route('/departments/<int:department>/items/<int:item_id>/JSON')
def itemsJSON(department_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)

#JSON for all departments 
@app.route('/department/JSON')
def departmentsJSON():
    departments = session.query(Department).all()
    return jsonify(departments=[r.serialize for r in departments])


# Show all departments
@app.route('/')
@app.route('/veganmarket/')
def showDepartments():
    departments = session.query(Department).all()
    return render_template('departments.html', departments=departments)


# Create a new department
@app.route('/departments/new/', methods=['GET', 'POST'])
def newDepartment():

    if request.method == 'POST':
        newDepartment = Department(name=request.form['name'], image=request.form['image'])
        try:
            session.add(newDepartment)
            flash('Department %s added successfully ' % newDepartment.name)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close() 
        return redirect(url_for('showDepartments'))
    else:
        return render_template('newDepartment.html')




# Edit a department
@app.route('/departments/<int:department_id>/edit/', methods=['GET', 'POST'])
def editDepartment(department_id):
    editedDepartment = session.query(Department).filter_by(id=department_id).one()
    if request.method == 'POST':
            editedDepartment.name = request.form['name']
            editedDepartment.image=request.form['image']
            return redirect(url_for('showDepartments'))
    else:
        return render_template(
            'editDepartment.html', department=editedDepartment)


#show items in a department
@app.route('/departments/<int:department_id>/')
@app.route('/departments/<int:departments>/items/')
def showItems(department_id):
    department = session.query(Department).filter_by(id=department_id).one()
    items = session.query(Item).filter_by(
        department_id=department_id).all()
    return render_template('items.html', items=items, department=department)
  

#Delete department
@app.route('/departments/<int:department_id>/delete/', methods=['GET', 'POST'])
def deleteDepartment(department_id):
    unwantedDepartment = session.query(
        Department).filter_by(id=department_id).one()
    if request.method == 'POST':
        try:
            session.delete(unwantedDepartment)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close() 
        return redirect(
            url_for('showDepartments', department_id=department_id))
    else:
        return render_template(
            'deleteDepartment.html', department=unwantedDepartment)
   
#create new items in departments
@app.route('/departments/<int:department_id>/new/', methods=['GET', 'POST'])
def newItem(department_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
        description=request.form['description'], 
        price=request.form['price'], department_id=department_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItems', department_id=department_id))
    else:
        return render_template('newItem.html', department_id=department_id)

 
# Edit an item


@app.route('/department/<int:department_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(department_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItems', department_id=department_id))
    else:

        return render_template(
            'editItem.html', department_id=department_id, item_id=item_id, item=editedItem)

# Delete an item


@app.route('/department/<int:department_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(department_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', department_id=department_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)
   



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
