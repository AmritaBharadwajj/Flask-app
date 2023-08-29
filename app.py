import os
from threading import Thread
from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from passlib.hash import pbkdf2_sha256
from flask_oauthlib.provider import OAuth2Provider
from passlib.hash import pbkdf2_sha256

import requests

from api.google_auth import create_google_oauth_flow, get_authenticated_service, get_user_info

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
oauth = OAuth2Provider(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    tokens = db.relationship('OAuth2Token', backref='user', lazy=True)

class OAuth2Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True, nullable=False)
#@app.route('/')
#def root():
    #return("LOL")
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/google/login')
def googleLogin():
    redirect_uri = 'http://localhost'
    flow = create_google_oauth_flow(redirect_uri)
    credentials = flow.run_local_server(port=0)
    authenticated_service = get_authenticated_service(credentials)
    user_info = get_user_info(authenticated_service)
    
    print("User's Google ID:", user_info.get('id'))
    print("User's Name:", user_info.get('name'))
    print("User's Email:", user_info.get('email'))

    return "User's Google ID: " + user_info.get('id') + "    User's Name:" + user_info.get('name') + "   User's Email:" + user_info.get('email')
   


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin_user = User.query.filter_by(username='admin').first()
        if(admin_user is None):
            admin_user = User(username='admin', password=pbkdf2_sha256.hash("333"))
            db.session.add(admin_user)
            db.session.commit()

app.config['GOOGLE_API_KEY'] = 'google_api_key'
@app.route('/fetch_google_drive_data')
def fetch_google_drive_data():
    google_api_key = app.config['GOOGLE_API_KEY']
    url = f'https://www.googleapis.com/drive/v3/files?key={google_api_key}'

    response = requests.get(url)
    data = response.json()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)









    app.run(debug=True)
