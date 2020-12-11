from flask import flash, render_template, request, redirect, url_for
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from .models import *
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from datetime import datetime
import csv
import pandas as pd

static = os.path.join(app.root_path, 'static/')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    students = Students.query.all()
    prospects = Prospects.query.all()
    exstudents = Exstudents.query.all()
    return render_template("index.html", prospects=prospects, students=students, exstudents=exstudents)


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
        if request.form['password'] == request.form['copassword']:
            user = User.query.get_or_404(id)
            user.firstname = request.form['firstname']
            user.lastname = request.form['lastname']
            if current_user.id == id:
                pass
            else:
                user.role = request.form['role']
            if request.form['password'] == '':
                pass
            else:
                hashed_password = generate_password_hash(request.form["password"] , method='sha256')
                user.password = hashed_password

            db.session.commit()

            flash("User " + user.firstname + ' ' + user.lastname + " has been successfully edited")
        else:
            flash('Opps! Password mismatch . . .')
        if current_user.id == id:
            return redirect(url_for('settings'))
        else:
            return redirect(url_for('users'))
    else:
        return redirect(request.url)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')

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
    if category == 'prospects':
        clients = Prospects.query.all()
    elif category == 'students':
        clients = Students.query.all()
    elif category == 'exstudents':
        clients = Exstudents.query.all()
    return render_template('customers.html', category=category, clients=clients, totalcount=clients)



@app.route('/filter/<category>', methods=['GET', 'POST'])
@login_required
def filter(category):
    if request.method == 'POST':
        search = request.form['keyword']
        if search == 'Balanced':
            if category == 'students':
                clients = Students.query.filter_by(balance = 0).all()
        elif search == 'Outstanding':
            if category == 'students':
                clients = Students.query.filter(Students.balance > 0).all()
        else:
            if category == 'prospects':
                clients = Prospects.query.filter(or_(Prospects.fullname.ilike(f'%{search}%'), Prospects.email.ilike(f'%{search}%'), Prospects.phone.ilike(f'%{search}%'), Prospects.location.ilike(f'%{search}%'), Prospects.sector.ilike(f'%{search}%'), Prospects.status.ilike(f'%{search}%'), Prospects.remark.ilike(f'%{search}%'), Prospects.extra1.ilike(f'%{search}%'), Prospects.extra2.ilike(f'%{search}%'), Prospects.extra3.ilike(f'%{search}%'))).all()
            elif category == 'students':
                clients = Students.query.filter(or_(Students.fullname.ilike(f'%{search}%'), Students.email.ilike(f'%{search}%'), Students.phone.ilike(f'%{search}%'), Students.location.ilike(f'%{search}%'), Students.courses.ilike(f'%{search}%'), Students.registration_fee.ilike(f'%{search}%'), Students.tutorial_fee.ilike(f'%{search}%'), Students.course_fee.ilike(f'%{search}%'), Students.payment_1.ilike(f'%{search}%'), Students.payment_2.ilike(f'%{search}%'), Students.payment_3.ilike(f'%{search}%'), Students.balance.ilike(f'%{search}%'), Students.exam.ilike(f'%{search}%'), Students.remark_1.ilike(f'%{search}%'), Students.remark_2.ilike(f'%{search}%'), Students.extra1.ilike(f'%{search}%'), Students.extra2.ilike(f'%{search}%'), Students.extra3.ilike(f'%{search}%'))).all()
            elif category == 'exstudents':
                clients = Exstudents.query.filter(or_(Exstudents.fullname.ilike(f'%{search}%'), Exstudents.email.ilike(f'%{search}%'), Exstudents.phone.ilike(f'%{search}%'), Exstudents.location.ilike(f'%{search}%'), Exstudents.courses.ilike(f'%{search}%'), Exstudents.balance.ilike(f'%{search}%'), Exstudents.results.ilike(f'%{search}%'), Exstudents.referral_name.ilike(f'%{search}%'), Exstudents.referral_number.ilike(f'%{search}%'), Exstudents.referral_email.ilike(f'%{search}%'), Exstudents.remark.ilike(f'%{search}%'), Exstudents.extra1.ilike(f'%{search}%'), Exstudents.extra2.ilike(f'%{search}%'), Exstudents.extra3.ilike(f'%{search}%'))).all()
        if category == 'prospects':
            totalcount = Prospects.query.all()
        if category == 'students':
            totalcount = Students.query.all()
        if category == 'exstudents':
            totalcount = Exstudents.query.all()
        return render_template('customers.html', category=category, clients=clients, search=search, totalcount=totalcount)
    else:
        return redirect(url_for('index'))


@app.route('/edit-client/<category>/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(category, id):
    if request.method == 'POST':
        if request.form['extra1'] == 'None':
            extra1 = ''
        else:
            extra1 = request.form['extra1']
        if request.form['extra2'] == 'None':
            extra2 = ''
        else:
            extra2 = request.form['extra2']
        if request.form['extra3'] == 'None':
            extra3 = ''
        else:
            extra3 = request.form['extra3']
        if category == 'prospects':
            client = Prospects.query.get_or_404(id)
            client.fullname = request.form['fullname']
            client.email = request.form['email']
            client.phone = int(request.form['phone'])
            client.location = request.form['location']
            client.sector = request.form['sector']
            client.status = request.form['status']
            client.remark = request.form['remark']
            client.extra1 = extra1
            client.extra2 = extra2
            client.extra3 = extra3
        elif category == 'students':
            client = Students.query.get_or_404(id)
            client.fullname = request.form['fullname']
            client.email = request.form['email']
            client.phone = int(request.form['phone'])
            client.location = request.form['location']
            client.courses = request.form['courses']
            client.registration_fee = int(request.form['registration_fee'])
            client.tutorial_fee = int(request.form['tutorial_fee'])
            client.course_fee = int(request.form['course_fee'])
            if request.form['payment_1'] == '' or request.form['payment_1'] == ' ':
                payment_1 = 0
            else:
                payment_1 = request.form['payment_1']
            if request.form['payment_2'] == '' or request.form['payment_2'] == ' ':
                payment_2 = 0
            else:
                payment_2 = request.form['payment_2']
            if request.form['payment_3'] == '' or request.form['payment_3'] == ' ':
                payment_3 = 0
            else:
                payment_3 = request.form['payment_3']
            client.payment_1 = int(payment_1)
            client.payment_2 = int(payment_2)
            client.payment_3 = int(payment_3)
            client.balance = (int(request.form['course_fee'])) - (int(payment_1) + int(payment_2) + int(payment_3))
            client.exam = request.form['exam']
            client.remark_1 = request.form['remark_1']
            client.remark_2 = request.form['remark_2']
            client.extra1 = extra1
            client.extra2 = extra2
            client.extra3 = extra3
        elif category == 'exstudents':
            client = Exstudents.query.get_or_404(id)
            client.fullname = request.form['fullname']
            client.email = request.form['email']
            client.phone = int(request.form['phone'])
            client.location = request.form['location']
            client.courses = request.form['courses']
            client.balance = request.form['balance']
            client.results = request.form['results']
            client.referral_name = request.form['referral_name']
            client.referral_number = request.form['referral_number']
            client.referral_email = request.form['referral_email']
            client.remark = request.form['remark']
            client.extra1 = extra1
            client.extra2 = extra2
            client.extra3 = extra3
        db.session.commit()
        flash('Edited ' + str(client.fullname) + ' a client from ' + str(category))
        new_url = '/customers/' + category
        return redirect(new_url)
    else:
        new_url = '/customers/' + category
        return redirect(new_url)

@app.route('/delete-customer/<category>/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_customer(category, id):
    if category == 'prospects':
        client = Prospects.query.get_or_404(id)
    elif category == 'students':
        client = Students.query.get_or_404(id)
    elif category == 'exstudents':
        client = Exstudents.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(client)
        db.session.commit()
        flash('Deleted a client from ' + str(category))
        new_url = '/customers/' + category
        return redirect(new_url)
    else:
        return render_template('delete.html', category=category, client=client)


# the below function is to verify if the uploaded file is an xls, xlsx or csv file
def validate_xlfiles(xlfile):
    f_name, f_ext = os.path.splitext(xlfile.filename)
    if f_ext.upper() in ['.XLSX', '.XLS', '.CSV']:
        return True
    else:
        return 'File must be xls, xlsx, csv'

def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict

@app.route('/export', methods=['GET', 'POST'])
@login_required
def exportfile():
    if request.method == 'POST':
        category = request.form['category']
        if category == '0':
            flash('Please select a category')
        else:            
            file_obj = 'data/newCDMS.xlsx'
            file_name = static + file_obj
            # file_name = url_for('static', filename='data/newCDMS.xlsx')
            # file_name = app.config['DATA_FOLDER']+'newCDMS.xlsx' 
            if category.lower() == 'mixed':     
                data_fetched = pd.DataFrame([to_dict(item) for item in Prospects.query.all()])
                data_fetched2 = pd.DataFrame([to_dict(item) for item in Students.query.all()])
                data_fetched3 = pd.DataFrame([to_dict(item) for item in Exstudents.query.all()])
                sheets = {'PROSPECT': data_fetched, 'STUDENTS': data_fetched2, 'EX-STUDENT': data_fetched3}
                writer = pd.ExcelWriter(file_name)

                for sheet in sheets.keys():
                    sheets[sheet].to_excel(writer, sheet_name=sheet, index=False)
                writer.save()
                flash('Downloadable File generated for download')
            else:
                if category.lower() == 'prospect':
                    data_fetched = pd.DataFrame([to_dict(item) for item in Prospects.query.all()])
                elif category.lower() == 'students':
                    data_fetched = pd.DataFrame([to_dict(item) for item in Students.query.all()])
                elif category.lower() == 'ex-student':
                    data_fetched = pd.DataFrame([to_dict(item) for item in Exstudents.query.all()])
                sheet = category.upper()
                data_fetched.to_excel(file_name, sheet_name=sheet, index=False)
                flash('Downloadable File generated for download')
            return render_template('export.html', file_name=file_obj)
    return render_template('export.html')

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
                files = pd.read_excel(xlfile, sheet_name=None, header=0)
                for sheet, data in files.items():
                    dfs = pd.read_excel(xlfile, sheet_name=sheet, header=0)
                #     print(dfs.to_dict())
                    if dfs['Email'].any():
                        length = dfs['Email']
                    else:
                        length = dfs['S/N']
                    for i in range(0, len(length)):
                        if sheet.lower() == 'prospect':
                            check_data_exist = 0
                            for items in Prospects.query.filter_by(email=dfs['Email'][i]):
                                check_data_exist += 1
                            if check_data_exist == 0:
                                # print(dfs['Email'][i], ' not found in db . . .Proceed . . .')
                                new_data_input = Prospects(fullname=dfs['Full-Name'][i], email=dfs['Email'][i], phone=int(dfs['Phone'][i]), location=dfs['Location'][i], sector=dfs['Sector'][i], status=dfs['Status'][i], remark=dfs['Remark'][i], extra1=dfs['Extra1'], extra2=dfs['Extra2'], extra3=dfs['Extra3'])             
                                db.session.add(new_data_input)
                                db.session.commit()      
                            # else:
                            #     print('Found ', dfs['Email'][i], ' in db')         
                        elif sheet.lower() == 'students':
                            check_data_exist = 0
                            for items in Students.query.filter_by(email=dfs['Email'][i]):
                                check_data_exist += 1
                            if check_data_exist == 0:
                                # print(dfs['Email'][i], ' not found in db . . .Proceed . . .')
                                new_data_input = Students(fullname=dfs['Full-Name'][i], email=dfs['Email'][i], phone=int(dfs['Phone'][i]), location=dfs['Location'][i], courses=dfs['Course-Name'][i], registration_fee=int(dfs['Registration-Fee'][i]), tutorial_fee=int(dfs['Tutorial-Fee'][i]), course_fee=int(dfs['Course-Fee'][i]), payment_1=int(dfs['1st-Payment'][i]), payment_2=int(dfs['2nd-Payment'][i]), payment_3=int(dfs['3rd-Payment'][i]), balance=int(dfs['Balance'][i]), exam=dfs['Exam'][i], remark_1=dfs['Remark-1'][i], remark_2=dfs['Remark-2'][i], extra1=dfs['Extra1'], extra2=dfs['Extra2'], extra3=dfs['Extra3'])             
                                db.session.add(new_data_input)
                                db.session.commit()      
                            # else:
                            #     print('Found ', dfs['Email'][i], ' in db')
                        elif sheet.lower() == 'ex-student':
                            check_data_exist = 0
                            for items in Exstudents.query.filter_by(email=dfs['Email'][i]):
                                check_data_exist += 1
                            if check_data_exist == 0:
                                # print(dfs['Email'][i], ' not found in db . . .Proceed . . .')
                                new_data_input = Exstudents(fullname=dfs['Full-Name'][i], email=dfs['Email'][i], phone=int(dfs['Phone'][i]), location=dfs['Location'][i], courses=dfs['Course-Name'][i], balance=int(dfs['Balance'][i]), results=dfs['Results'][i], referral_name=dfs['Referral-Name'][i], referral_number=int(dfs['Referral-Number'][i]), referral_email=dfs['Referral-Email'][i], remark=dfs['Remark'][i], extra1=dfs['Extra1'], extra2=dfs['Extra2'], extra3=dfs['Extra3'])             
                                db.session.add(new_data_input)
                                db.session.commit()      
                            # else:
                            #     print('Found ', dfs['Email'][i], ' in db')  
                flash("Successful Upload")
                return render_template('import.html')
            else:
                flash(validate_xlfiles(xlfile))
    return render_template('import.html')

@app.route('/add/<category>', methods=['GET', 'POST'])
@login_required
def addclient(category):
    if request.method == 'POST':
        if request.form['extra1'] == 'None':
            extra1 = ''
        else:
            extra1 = request.form['extra1']
        if request.form['extra2'] == 'None':
            extra2 = ''
        else:
            extra2 = request.form['extra2']
        if request.form['extra3'] == 'None':
            extra3 = ''
        else:
            extra3 = request.form['extra3']
        if category.lower() == 'prospects':
            check_data_exist = 0
            for items in Prospects.query.filter_by(email=request.form['email']):
                check_data_exist += 1
            if check_data_exist == 0:
                new_data_input = Prospects(fullname=request.form['fullname'], email=request.form['email'], phone=int(request.form['phone']), location=request.form['location'], sector=request.form['sector'], status=request.form['status'], remark=request.form['remark'], extra1=extra1, extra2=extra2, extra3=extra3)             
                db.session.add(new_data_input)
                db.session.commit()      
            # else:
            #     print('Found ', dfs['Email'][i], ' in db')         
        elif category.lower() == 'students':
            check_data_exist = 0
            for items in Students.query.filter_by(email=request.form['email']):
                check_data_exist += 1
            if check_data_exist == 0:
                # print(request.form['email'], ' not found in db . . .Proceed . . .')
                new_data_input = Students(fullname=request.form['fullname'], email=request.form['email'], phone=int(request.form['phone']), location=request.form['location'], courses=request.form['courses'], registration_fee=int(request.form['registration_fee']), tutorial_fee=int(request.form['tutorial_fee']), course_fee=int(request.form['course_fee']), payment_1=int(request.form['payment_1']), payment_2=int(request.form['payment_2']), payment_3=int(request.form['payment_3']), balance=(int(request.form['course_fee'])) - (int(request.form['payment_1']) + int(request.form['payment_2']) + int(request.form['payment_3'])), exam=request.form['exam'], remark_1=request.form['remark_1'], remark_2=request.form['remark_2'], extra1=extra1, extra2=extra2, extra3=extra3)             
                db.session.add(new_data_input)
                db.session.commit()      
            # else:
            #     print('Found ', request.form['email'], ' in db')
        elif category.lower() == 'exstudents':
            check_data_exist = 0
            for items in Exstudents.query.filter_by(email=request.form['email']):
                check_data_exist += 1
            if check_data_exist == 0:
                # print(request.form['email'], ' not found in db . . .Proceed . . .')
                new_data_input = Exstudents(fullname=request.form['fullname'], email=request.form['email'], phone=int(request.form['phone']), location=request.form['location'], courses=request.form['courses'], balance=int(request.form['balance']), results=request.form['results'], referral_name=request.form['referral_name'], referral_number=int(request.form['referral_number']), referral_email=request.form['referral_email'], remark=request.form['remark'], extra1=extra1, extra2=extra2, extra3=extra3)             
                db.session.add(new_data_input)
                db.session.commit()      
            # else:
            #     print('Found ', dfs['Email'][i], ' in db')  
        flash("Client Successfully added")
    new_url = '/customers/' + category
    return redirect(new_url)

@app.errorhandler(404)
def page_notfound(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

