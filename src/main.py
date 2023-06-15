# File: src/main.py
from flask import Flask
from flask_restx import Api

from api import azure
from api.deploy import deploy_ns
from api.vpn import vpn_ns
from tasks.taskScheduler import start_tasks


def create_app():
    app = Flask(__name__)
    api = Api(app, title='SagaLabs Backbone API', version='1.0')

    api.add_namespace(azure.azure_ns, path='/api/azure')
    api.add_namespace(deploy_ns, path='/api/deploy')
    api.add_namespace(vpn_ns, path='/api/vpn')

    # Start the scheduled tasks
    start_tasks()

    return app
