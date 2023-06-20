# __init__.py
# main file
import os

from flask import Flask, url_for, request, jsonify, abort, send_from_directory

from flask_restx import Api

from .api.azure import azure_ns
from .api.deploy import deploy_ns
from .api.vpn import vpn_ns
from .authentication.auth import auth
from .authentication.login import login
from .authentication import setCookie, debugCookie, logout
from .authentication import firebase  # import here to ensure Firebase is initialized first


def create_app():
    app = Flask(__name__)

    authorizations = {
        'Server Key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
    }

    api = Api(app, title='SagaLabs Backbone API', version='1.0', authorizations=authorizations,
              decorators=[auth.login_required], security='Server authentication')

    api.add_namespace(azure_ns, path='/api/azure')
    api.add_namespace(deploy_ns, path='/api/deploy')
    api.add_namespace(vpn_ns, path='/api/vpn')

    # Add the login, set_cookie, and debug_cookie routes to the Flask app
    app.add_url_rule('/login', 'login', login, methods=['GET'])
    app.add_url_rule('/login/set_cookie', 'set_cookie', setCookie.set_cookie, methods=['POST'])
    app.add_url_rule('/login/debugCookie', 'debug_cookie', debugCookie.debug_cookie, methods=['GET'])
    app.add_url_rule('/logout', 'logout', logout.logout, methods=['GET'])

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'sagalabs.png', mimetype='image/vnd.microsoft.icon')

    return app
