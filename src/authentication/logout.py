# authentication/logout.py
from flask import make_response, redirect, url_for


def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('sagalabs_auth', '', expires=0)
    return response
