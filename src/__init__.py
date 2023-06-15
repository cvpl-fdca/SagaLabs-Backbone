# __init__.py
from flask import Flask

from flask_restx import Api

from .api.azure import azure_ns
from .api.deploy import deploy_ns
from .api.vpn import vpn_ns
from .authentication.auth import auth


def create_app():
    app = Flask(__name__)

    authorizations = {
        'Server authentication': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

    api = Api(app, title='SagaLabs Backbone API', version='1.0', authorizations=authorizations,
              decorators=[auth.login_required], prefix="/api", security='Server authentication')

    api.add_namespace(azure_ns, path='/azure')
    api.add_namespace(deploy_ns, path='/deploy')
    api.add_namespace(vpn_ns, path='/vpn')

    return app
