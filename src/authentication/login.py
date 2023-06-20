from flask import request, redirect, make_response, render_template
from firebase_admin import auth
import src.authentication.firebase



def login():
    return render_template('firebaseLogin/login.html')
