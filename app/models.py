
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


# class Complaints(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
#     complain = db.Column(db.Text)
#     status = db.Column(db.String)

#     def __repr__(self):
#         return 'Complaints ' + str(self.id)

