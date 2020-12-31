
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from dotenv import load_dotenv
import os 

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = 'SCreytkri'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/timetable'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['DATA_FOLDER'] = 'static/data/'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# flask db init
# flask db migrate -m 'Initial Migrate'
# flask db upgrade

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models

if __name__ == '__main__':
    manager.run()
