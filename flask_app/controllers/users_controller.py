from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('register_login.html')

@app.route('/registration', methods = ['POST'])
def registration():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    users_id = User.save(data)
    session['user_id'] = users_id
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    login_user = User.check_email(data)
    if not login_user:
        flash("Invalid e-mail, try again", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(login_user.password, request.form['password']):
        flash("Invalid password, try again", "login")
        return redirect('/')
    session['user_id'] = login_user.id
    session['users'] = login_user.first_name
    return redirect('/dashboard')

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')