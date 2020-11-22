from flask import flash, render_template, request, redirect, url_for
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from .models import *
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    return render_template("index.html")

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email = request.form["email"]).first()

        if user:
            if check_password_hash(user.password, request.form["password"]):
                login_user(user)
                
                flash('Welcome '+ user.lastname+' '+user.firstname)
                return redirect(url_for('index'))
            else:
                flash ('Invalid Credentials')
    
    admin = User.query.filter_by(email = 'admin@admin.com').first()
    if admin:
        pass
    else:
        hashed_password = generate_password_hash('admin' , method='sha256')

        lastname = 'Admin'
        firstname = 'Admin'
        role = 'Admin'
        email = 'admin@admin.com'
        password = hashed_password

        new_admin = User(lastname=lastname, firstname=firstname, role=role, email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()
    
    return render_template('login.html', title = 'Login',)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create-user', methods=['GET', 'POST'])
@login_required
def createuser():
    if request.method == "POST":
        hashed_password = generate_password_hash(request.form["password"] , method='sha256')

        lastname = request.form["lastname"]
        firstname = request.form["firstname"]
        periods = request.form["periods"]
        role = request.form["role"]
        email = request.form["email"]
        password = hashed_password

        new_user = User(lastname=lastname, firstname=firstname, role=role, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Educator Registration Successful!')
        return redirect(url_for('controlpanel'))

@app.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
def edituser(id):
    if request.method == 'POST':
        user = User.query.get_or_404(id)
        user.firstname = request.form['firstname']
        user.lastname = request.form['lastname']
        user.role = request.form['role']
        user.periods = request.form['periods']
        user.email = request.form['email']
        if request.form['password'] == '':
            pass
        else:
            hashed_password = generate_password_hash(request.form["password"] , method='sha256')
            user.password = hashed_password

        db.session.commit()

        flash("User " + user.firstname + ' ' + user.lastname + " has been successfully edited")
        return redirect(url_for('controlpanel'))
    return redirect(request.url)

@app.route('/delete-user/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteuser(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    flash("Deleted Educator")
    return redirect(url_for('controlpanel'))


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.firstname = request.form['firstname']
        current_user.lastname = request.form['lastname']
        current_user.email = request.form['email']
        if request.form['password'] == '':
            pass
        else:
            hashed_password = generate_password_hash(request.form["password"] , method='sha256')
            current_user.password = hashed_password

        db.session.commit()

        flash("User " + current_user.firstname + ' ' + current_user.lastname + " has been successfully edited")
        return redirect(url_for('settings'))

    return render_template('settings.html')

    

@app.errorhandler(404)
def page_notfound(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

