from flask import Flask, render_template, url_for, request, session, redirect, flash
# from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing'

# app.config['MONGO_dbname'] = 'users'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017'
mongo = MongoClient('localhost', 27017)
# mongo = PyMongo(app)

@app.route("/")
@app.route("/main")
def main():
    return render_template('index.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        signup_user = users.find_one({'username': request.form['username']})
        print(signup_user)
        if signup_user:
            flash(request.form['username'] + ' username is already exist')
            return redirect(url_for('signup'))
        
        users.insert_one({'username': request.form['username'], 'password': request.form['password'], 'email': request.form['email']})
        return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])

    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        users = mongo.db.users
        signin_user = users.find_one({'username': request.form['username']})
        
        if signin_user:
            if request.form['password'] == signin_user['password']:
                session['username'] = request.form['username']
                return redirect('http://172.17.12.213:5000')

        flash('Username and password combination is wrong')
        return render_template('signin.html')

    return render_template('signin.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    app.run()
