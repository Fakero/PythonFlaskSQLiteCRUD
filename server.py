import json
import dbconnection
from flask import Flask, request, Response, render_template
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

@app.route('/users/newuser', methods = ['POST'])
def new_user():
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

@app.route('/users/all')
def get_users():
    init_list()
    return render_template('users.html', result = users)

@app.route('/users/alljson')
def get_users_json():
    init_list()
    u = json.dumps(users, indent=True)
    resp = Response(u, status=200, mimetype='application/json')
    return resp

@app.route('/users/delete', methods = ['DELETE'])
def delete_user():
    user = request.get_json(force = True)
    dbconnection.sqlite_connection.init_app(app)
    dbconnection.sqlite_connection.connection.execute('''DELETE FROM Users WHERE Id = ? ''', (user['id'],))
    dbconnection.sqlite_connection.commit()
    dbconnection.sqlite_connection.close_connection()
    return "Success!"

@app.route('/users/<username>')
def get_user(username):
    dbconnection.sqlite_connection.init_app(app)
    cursor = dbconnection.sqlite_connection.get_cursor()
    cursor.execute('''SELECT * FROM Users WHERE Username = ? ''', (username,))
    dbconnection.sqlite_connection.commit()
    row = cursor.fetchone()
    return json.dumps({"id":row[0], "username":row[1], "password":row[2], "firstname":row[3], "lastname":row[4]}, indent=True)

@app.route('/users/update', methods = ['PUT'])
def update_user():
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


if __name__ == '__main__':
    app.run(debug = True)


