# authentication/auth.py
from flask import request
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized
import os

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    # Bypass authentication for Swagger UI
    if request.path == '/swagger.json' or request.path.startswith('/login'):
        return True
    # os.getenv('SERVER_TOKEN')
    server_token = os.getenv("SERVER_TOKEN")
    if not server_token:
        raise Unauthorized('Server token not found in environment variables')
    return token == server_token
