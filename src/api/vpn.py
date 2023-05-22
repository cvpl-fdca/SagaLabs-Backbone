from flask import jsonify
from flask_restx import Namespace, Resource
import requests
from base64 import b64encode
from dotenv import load_dotenv
import os

from api.azure import PublicIPAddresses
from tasks.azure_tasks import get_resources

load_dotenv()

vpn_ns = Namespace('vpn', description='vpn related operations')


@vpn_ns.route('/<string:range_name>/users/get')
class GetVPNUsers(Resource):
    def get(self, range_name):
        # Get public IP addresses from all the labs within the range
        public_ip_resources = PublicIPAddresses().get(range_name)

        pass
