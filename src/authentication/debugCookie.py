# debugCookie.py
from firebase_admin import auth as firebaseauth, exceptions
from flask import jsonify, abort, request


def debug_cookie():
    # Get the session cookie from the request
    session_cookie = request.cookies.get('sagalabs_auth')

    try:
        # Verify the session cookie and check the user claims.
        decoded_claims = firebaseauth.verify_session_cookie(session_cookie)
        return jsonify(decoded_claims)
    except exceptions.FirebaseError:
        return abort(401, 'Failed to verify session cookie')
