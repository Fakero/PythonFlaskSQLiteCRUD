import json
import dbconnection
from flask import Flask, request, Response, render_template, redirect, url_for
app = Flask(__name__)

users = []

def init_list():
    users.clear()
    dbconnection.sqlite_connection.init_app(app)
    cursor = dbconnection.sqlite_connection.get_cursor()
    cursor.execute('''SELECT * FROM Users''')
    for row in cursor:
        user = {"id":row[0], "username":row[1], "password":row[2], "firstname":row[3], "lastname":row[4]}
        users.append(user)
    dbconnection.sqlite_connection.commit()
    dbconnection.sqlite_connection.close_connection()

# WEB UI

# index
@app.route('/users/all')
def get_users():
    init_list()
    return render_template('users.html', result = users)

# find user by id
@app.route('/users/<id>')
def edit_user(id):
    dbconnection.sqlite_connection.init_app(app)
    cursor = dbconnection.sqlite_connection.get_cursor()
    cursor.execute('''SELECT * FROM Users WHERE Id = ? ''', (id,))
    row = cursor.fetchone()
    user = {"id":row[0], "username":row[1], "password":row[2], "firstname":row[3], "lastname":row[4]}
    dbconnection.sqlite_connection.commit()
    dbconnection.sqlite_connection.close_connection()
    return render_template('user.html', user = user)

# new user form
@app.route('/users/newuser')
def new_user():
    return render_template('newuser.html')

# add user to database
@app.route('/users/newuser/add', methods = ['POST'])
def add_new_user():
    user = request.form
    dbconnection.sqlite_connection.init_app(app)
    cursor = dbconnection.sqlite_connection.get_cursor()
    uname = str(user['username'])
    pword = str(user['password'])
    fname = str(user['firstname'])
    lname = str(user['lastname'])
    cursor.execute('''INSERT INTO Users(Username, Password, Firstname, Lastname) VALUES(?, ?, ?, ?)''', (uname, pword, fname, lname))    
    dbconnection.sqlite_connection.commit()
    dbconnection.sqlite_connection.close_connection()
    return redirect(url_for('get_users'))

# update user information
@app.route('/users/update', methods = ['PUT', 'POST'])
def update_user():
    user = request.form
    dbconnection.sqlite_connection.init_app(app)
    cursor = dbconnection.sqlite_connection.get_cursor()
    uname = str(user['username'])
    pword = str(user['password'])
    fname = str(user['firstname'])
    lname = str(user['lastname'])
    cursor.execute('''UPDATE Users SET Username = ?, Password = ?, Firstname = ?, Lastname = ? WHERE Id = ? ''', (uname, pword, fname, lname, user['id']))
    dbconnection.sqlite_connection.commit()
    dbconnection.sqlite_connection.close_connection()
    return redirect(url_for('get_users'))

@app.route('/users/delete', methods = ['DELETE', 'POST'])
def delete_user():
    user = request.form
    dbconnection.sqlite_connection.init_app(app)
    dbconnection.sqlite_connection.connection.execute('''DELETE FROM Users WHERE Id = ? ''', (user['id'],))
    dbconnection.sqlite_connection.commit()
    dbconnection.sqlite_connection.close_connection()
    return redirect(url_for('get_users'))

# for easy routing
@app.route('/')
def index_site():
    return redirect(url_for('get_users'))

@app.route('/users')
def user_index():
    return redirect(url_for('get_users'))

# JSON, CRUD functions for postman testing

@app.route('/users/json/all')
def get_users_json():
    init_list()
    u = json.dumps(users, indent=True)
    resp = Response(u, status=200, mimetype='application/json')
    return resp

@app.route('/users/json/<username>')
def get_user_json(username):
    dbconnection.sqlite_connection.init_app(app)
    cursor = dbconnection.sqlite_connection.get_cursor()
    cursor.execute('''SELECT * FROM Users WHERE Username = ? ''', (username,))
    dbconnection.sqlite_connection.commit()
    row = cursor.fetchone()
    return json.dumps({"id":row[0], "username":row[1], "password":row[2], "firstname":row[3], "lastname":row[4]}, indent=True)

@app.route('/users/json/add', methods = ['POST'])
def add_new_user_json():
    user = request.get_json(force=True)
    dbconnection.sqlite_connection.init_app(app)
    cursor = dbconnection.sqlite_connection.get_cursor()
    uname = str(user['username'])
    pword = str(user['password'])
    fname = str(user['firstname'])
    lname = str(user['lastname'])
    cursor.execute('''INSERT INTO Users(Username, Password, Firstname, Lastname) VALUES(?, ?, ?, ?)''', (uname, pword, fname, lname))    
    dbconnection.sqlite_connection.commit()
    dbconnection.sqlite_connection.close_connection()
    return json.dumps(user, indent=True)

@app.route('/users/json/update', methods = ['PUT', 'POST'])
def update_user_json():
    user = request.get_json(force=True)
    dbconnection.sqlite_connection.init_app(app)
    cursor = dbconnection.sqlite_connection.get_cursor()
    uname = str(user['username'])
    pword = str(user['password'])
    fname = str(user['firstname'])
    lname = str(user['lastname'])
    cursor.execute('''UPDATE Users SET Username = ?, Password = ?, Firstname = ?, Lastname = ? WHERE Id = ? ''', (uname, pword, fname, lname, user['id']))
    dbconnection.sqlite_connection.commit()
    dbconnection.sqlite_connection.close_connection()
    return json.dumps(user, indent=True)

@app.route('/users/json/delete', methods = ['DELETE','POST'])
def delete_user_json():
    user = request.get_json(force = True)
    dbconnection.sqlite_connection.init_app(app)
    dbconnection.sqlite_connection.connection.execute('''DELETE FROM Users WHERE Id = ? ''', (user['id'],))
    dbconnection.sqlite_connection.commit()
    dbconnection.sqlite_connection.close_connection()
    return "Success!"

if __name__ == '__main__':
    app.run(debug = True)