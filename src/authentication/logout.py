# authentication/logout.py
from flask import make_response, redirect, url_for, request


def logout():
    redirect_url = request.args.get('redirect', '')
    response = make_response(redirect(url_for('login', redirect=redirect_url)))
    response.set_cookie('sagalabs_auth', '', expires=0)  # Deletes localhost and 127.0.0.1 cookie
    response.set_cookie('sagalabs_auth', '', expires=0, path='/', domain='.sagalabs.dk',
                        secure=True)  # Deletes cookie from backbone server
    return response
