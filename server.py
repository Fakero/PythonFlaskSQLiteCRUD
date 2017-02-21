import json
import dbservce
from flask import Flask, request, Response, render_template
app = Flask(__name__)

users = []

@app.route('/newuser/', methods = ['POST'])
def new_user():
    user = request.get_json(force=True)
    users.append(user)

@app.route('/getusers/')
def get_users():
    return render_template('users.html', result = users)

if __name__ == '__main__':
    app.run(debug = True)