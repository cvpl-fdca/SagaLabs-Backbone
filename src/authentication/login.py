# authentication/login.py
from flask import render_template

def login():
    return render_template('firebaseLogin/login.html')