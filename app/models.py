
from app import db
from flask_login import UserMixin
from app import login_manager
from datetime import datetime



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    role = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False) 
    password = db.Column(db.String(100)) 
    student = db.relationship('Offers', backref='student', lazy=True)
    # complains = db.relationship('Complaints', backref='author', lazy=True)

    def __init__(self, firstname, lastname, role, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Prospects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.Text, default=" ")
    email = db.Column(db.String)
    phone = db.Column(db.String, default=" ")
    location = db.Column(db.String, default=" ")
    data_source = db.Column(db.String, default=" ")
    sector = db.Column(db.String, default=" ")
    company_name = db.Column(db.String, default=" ")
    courses = db.Column(db.String, default=" ")
    status = db.Column(db.String, default=" ")
    remark = db.Column(db.Text, default=" ")
    extra1 = db.Column(db.Text, default=" ") 
    extra2 = db.Column(db.Text, default=" ") 
    extra3 = db.Column(db.Text, default=" ")     
    extra4 = db.Column(db.Text, default=" ")     
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Prospect ' + str(self.id)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.Text, default=" ")
    email = db.Column(db.String)
    phone = db.Column(db.String, default=" ")
    location = db.Column(db.String, default=" ")
    dob = db.Column(db.String, default=" ")
    courses = db.Column(db.Text, default=" ")
    registration_fee = db.Column(db.Integer, default=" ")
    tutorial_fee = db.Column(db.Integer, default=" ")
    course_fee = db.Column(db.Integer, default=" ")
    payment_1 = db.Column(db.Integer, default=" ")
    payment_2 = db.Column(db.Integer, default=" ")
    payment_3 = db.Column(db.Integer, default=" ")
    balance = db.Column(db.Integer, default=" ")
    exam = db.Column(db.String, default=" ")
    remark_1 = db.Column(db.Text, default=" ")
    remark_2 = db.Column(db.Text, default=" ")
    extra1 = db.Column(db.Text, default=" ") 
    extra2 = db.Column(db.Text, default=" ") 
    extra3 = db.Column(db.Text, default=" ") 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Student ' + str(self.id)

class Exstudents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.Text, default=" ")
    email = db.Column(db.String)
    phone = db.Column(db.String, default=" ")
    location = db.Column(db.String, default=" ")
    courses = db.Column(db.Text, default=" ")
    balance = db.Column(db.Integer, default=" ")
    results = db.Column(db.Text, default=" ")
    referral_name = db.Column(db.String, default=" ")
    referral_number = db.Column(db.String, default=" ")
    referral_email = db.Column(db.String, default=" ")
    remark = db.Column(db.Text, default=" ")
    extra1 = db.Column(db.Text, default=" ") 
    extra2 = db.Column(db.Text, default=" ") 
    extra3 = db.Column(db.Text, default=" ") 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Exstudent ' + str(self.id)



class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, default=" ")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    course = db.relationship('Lessons', backref='course', lazy=True)
    course_offered = db.relationship('Offers', backref='course', lazy=True)

    def __repr__(self):
        return 'Courses ' + str(self.id)


class Lessons(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    title = db.Column(db.Text, default=" ")
    link = db.Column(db.Text, default=" ")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Lessons ' + str(self.id)


class Offers(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    status = db.Column(db.String, default=" ")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Offers ' + str(self.id)

