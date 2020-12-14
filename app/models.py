
from app import db
from flask_login import UserMixin
from app import login_manager



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    role = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False) 
    password = db.Column(db.String(100)) 
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
    fullname = db.Column(db.Text)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    location = db.Column(db.String)
    data_source = db.Column(db.String)
    sector = db.Column(db.String)
    company_name = db.Column(db.String)
    courses = db.Column(db.String)
    status = db.Column(db.String)
    remark = db.Column(db.Text)
    extra1 = db.Column(db.Text) 
    extra2 = db.Column(db.Text) 
    extra3 = db.Column(db.Text) 

    def __repr__(self):
        return 'Prospect ' + str(self.id)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.Text)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    location = db.Column(db.String)
    dob = db.Column(db.Date)
    courses = db.Column(db.Text)
    registration_fee = db.Column(db.Integer)
    tutorial_fee = db.Column(db.Integer)
    course_fee = db.Column(db.Integer)
    payment_1 = db.Column(db.Integer)
    payment_2 = db.Column(db.Integer)
    payment_3 = db.Column(db.Integer)
    balance = db.Column(db.Integer)
    exam = db.Column(db.String)
    remark_1 = db.Column(db.Text)
    remark_2 = db.Column(db.Text)
    extra1 = db.Column(db.Text) 
    extra2 = db.Column(db.Text) 
    extra3 = db.Column(db.Text) 

    def __repr__(self):
        return 'Student ' + str(self.id)

class Exstudents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.Text)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    location = db.Column(db.String)
    courses = db.Column(db.Text)
    balance = db.Column(db.Integer)
    results = db.Column(db.Text)
    referral_name = db.Column(db.String)
    referral_number = db.Column(db.String)
    referral_email = db.Column(db.String)
    remark = db.Column(db.Text)
    extra1 = db.Column(db.Text) 
    extra2 = db.Column(db.Text) 
    extra3 = db.Column(db.Text) 

    def __repr__(self):
        return 'Exstudent ' + str(self.id)

