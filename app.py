from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from helpers import auth
from datetime import datetime
from utils import db as db
app = Flask(__name__)

con = db.DatabaseConnection()
authenticator = auth.Auth(con)

execute_query = con.execute_query


app.secret_key = con.secret_key
app.config['SECRET_KEY'] = con.secret_key


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        uname = request.form['uname']
        email = request.form['email']
        pno = request.form['pno']
        password = request.form['password']
        passwordc = request.form['passwordc']
        if(password != passwordc):
            flash("Passwords do not match")
        else:
            data = {
                "uname":uname,
                "email":email,
                "pno":pno,
                "password":password
            }
            authenticator.register(data)

        
        # Insert data into the database
        # query = """
        #     INSERT INTO user (uid, uname, email, pno, addr, rdate)
        #     VALUES (%s, %s, %s, %s, %s, %s)
        # """
        # params = (uid, uname, email, pno, addr, rdate)
        # execute_query(query, params)

        

        # Flash a success message and redirect
        flash('User registered successfully!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        
        print(authenticator.login(email, password))

        
        # Insert data into the database
        # query = """
        #     INSERT INTO user (uid, uname, email, pno, addr, rdate)
        #     VALUES (%s, %s, %s, %s, %s, %s)
        # """
        # params = (uid, uname, email, pno, addr, rdate)
        # execute_query(query, params)

        

        # Flash a success message and redirect
        flash('Logged in!', 'success')
        return redirect(url_for('login'))
    return render_template('login.html')