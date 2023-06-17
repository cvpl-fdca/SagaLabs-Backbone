# __init__.py
import os

from flask import Flask, url_for
from flask import send_from_directory

from flask_restx import Api

from .api.azure import azure_ns
from .api.deploy import deploy_ns
from .api.vpn import vpn_ns
from .authentication.auth import auth


def create_app():
    app = Flask(__name__)

    # Import the login function here, after the app has been created
    from .authentication.login import login

    authorizations = {
        'Server authentication': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

    api = Api(app, title='SagaLabs Backbone API', version='1.0', authorizations=authorizations,
              decorators=[auth.login_required], security='Server authentication')

    api.add_namespace(azure_ns, path='/api/azure')
    api.add_namespace(deploy_ns, path='/api/deploy')
    api.add_namespace(vpn_ns, path='/api/vpn')

    # Add the login route to the Flask app
    app.add_url_rule('/login', 'login', login)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'sagalabs.png', mimetype='image/vnd.microsoft.icon')

    return app



