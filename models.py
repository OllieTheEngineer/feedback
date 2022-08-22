from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.String(20), 
                        unique=True, 
                        primary_key=True)
    password = db.Column(db.Text, 
                        nullable=False)
    email = db.Column(db.Email(50), 
                     unique=True, 
                     nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)

class Feedback(db.Model):

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, unique=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullble=False)
    username = db.Column(db.ForeignKey('users.username'))

