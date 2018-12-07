from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Department, Item
from flask import send_from_directory


app = Flask(__name__)
engine = create_engine('sqlite:///veganmarket.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()




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
