from flask import flash, render_template, request, redirect, url_for
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from .models import *
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
import csv
import pandas as pd


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


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if request.method == "POST":
        if request.form['password'] != request.form['confirm_password']:
            flash('Password Mismatch . . .')
        else:
            hashed_password = generate_password_hash(request.form["password"] , method='sha256')

            lastname = request.form["lastname"]
            firstname = request.form["firstname"]
            role = request.form["role"]
            email = request.form["email"]
            password = hashed_password
            countUser = 0
            if role == '0':
                flash('Select a role')
            else:
                for found in User.query.filter_by(email=email):
                    countUser += 1
                if countUser > 0:
                    flash('Email already registered')
                else:
                    new_user = User(lastname=lastname, firstname=firstname, role=role, email=email, password=password)
                    db.session.add(new_user)
                    db.session.commit()

                    flash('Educator Registration Successful!')
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
def edituser(id):
    if request.method == 'POST':
        user = User.query.get_or_404(id)
        user.firstname = request.form['firstname']
        user.lastname = request.form['lastname']
        user.role = request.form['role']
        if request.form['password'] == '':
            pass
        else:
            hashed_password = generate_password_hash(request.form["password"] , method='sha256')
            user.password = hashed_password

        db.session.commit()

        flash("User " + user.firstname + ' ' + user.lastname + " has been successfully edited")
        return redirect(url_for('users'))
    return redirect(request.url)

@app.route('/delete-user/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteuser(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    flash("Deleted User")
    return redirect(url_for('users'))


@app.route('/customers/<category>', methods=['GET', 'POST'])
@login_required
def customers(category):
    return render_template('customers.html', category=category)

# the below function is to verify if the uploaded file is an xls, xlsx or csv file
def validate_xlfiles(xlfile):
    f_name, f_ext = os.path.splitext(xlfile.filename)
    if f_ext.upper() in ['.XLSX', '.XLS', '.CSV']:
        return True
    else:
        return 'File must be xls, xlsx, csv'


@app.route('/import', methods=['GET', 'POST'])
@login_required
def importfile():
    if request.method == 'POST':
        category = request.form['category']
        category = category.lower()
        if category == '0':
            flash('Please choose a category')
        else:
            xlfile = request.files['file']
            if validate_xlfiles(xlfile) == True:
                dfs = pd.read_excel(xlfile, file_name=None, header=0)
                for table, df in dfs.items():
                    print(df.to_dict()) 
                flash("Successful Upload")
                return render_template('import.html')
            else:
                flash(validate_xlfiles(xlfile))
    return render_template('import.html')

@app.errorhandler(404)
def page_notfound(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

