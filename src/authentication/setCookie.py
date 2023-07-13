# authentication/setCookie.py
from datetime import timedelta, datetime

from firebase_admin import exceptions, auth as firebaseauth
from flask import jsonify, abort, request, redirect, session


def set_cookie():
    # Get the ID token sent by the client
    id_token = request.json['idToken']
    # Set session expiration to 5 days.
    expires_in = timedelta(days=5)
    try:
        # Create the session cookie. This will also verify the ID token in the process.
        # The session cookie will have the same claims as the ID token.
        session_cookie = firebaseauth.create_session_cookie(id_token, expires_in=expires_in)
        response = jsonify({'status': 'success'})
        # Set cookie policy for session cookie.
        expires = datetime.now()
        expires = expires + expires_in
        host = request.headers.get('Host')
        if 'localhost' in host or '127.0.0.1' in host:
            cookie_domain = None
        else:
            cookie_domain = '.sagalabs.dk'
        response.set_cookie(
            'sagalabs_auth', session_cookie, expires=expires, httponly=True, secure=True, domain=cookie_domain)

        # Redirect the user to their original URL
        return response
    except exceptions.FirebaseError:
        return abort(401, 'Failed to create a session cookie')

