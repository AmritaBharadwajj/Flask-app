from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    google_id = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    tokens = db.relationship('OAuth2Token', backref='user', lazy=True)

class OAuth2Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True, nullable=False)
# models.py
class ActivityEvent(db.Model):
    __tablename__ = 'activity_event'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(50))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))


from app import db

class GoogleDriveData(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    
    time = db.Column(db.String(30))
    unique_qualifier = db.Column(db.String(50))
    application_name = db.Column(db.String(50))
    customer_id = db.Column(db.String(20))
    email = db.Column(db.String(100))
    profile_id = db.Column(db.String(50))
    ip_address = db.Column(db.String(20))
    event_type = db.Column(db.String(50))
    event_name = db.Column(db.String(50))
    alert_id = db.Column(db.String(100))


    def __repr__(self):
        return f'<GoogleDriveData {self.id}>'
