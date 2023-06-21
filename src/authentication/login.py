# authentication/login.py
from flask import request, redirect, make_response, render_template, session
from firebase_admin import auth, exceptions
from functools import wraps


def check_cookie_validity(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the session cookie from the request
        session_cookie = request.cookies.get('sagalabs_auth')

        # If the session_cookie is None or empty, call the original function
        if not session_cookie:
            return f(*args, **kwargs)

        try:
            # Verify the session cookie
            decoded_claims = auth.verify_session_cookie(session_cookie)
            redirect_url = session.get('redirect_url')

            if redirect_url:
                # Clear the redirect URL from the session
                session.pop('redirect_url')
                return redirect(redirect_url)
            else:
                return render_template('firebaseLogin/loggedin.html')
        except exceptions.FirebaseError:
            return f(*args, **kwargs)

    return decorated_function


@check_cookie_validity
def login():
    # When the user attempts to login, store the redirect URL in the session
    redirect_url = request.args.get('redirect', default=None, type=str)
    if redirect_url:
        session['redirect_url'] = redirect_url
    return render_template('firebaseLogin/login.html')
