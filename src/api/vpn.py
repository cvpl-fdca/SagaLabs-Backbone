from flask import jsonify
from flask_restx import Namespace, Resource
import requests
from base64 import b64encode
from dotenv import load_dotenv
import os

from api.azure import VpnPublicIPAddresses
from utils import ConfigManager, AzKeyvault


load_dotenv()

vpn_ns = Namespace('vpn', description='vpn related operations')


@vpn_ns.route('/<string:range_name>/users/get')
class GetVPNUsers(Resource):
    def get(self, range_name):
        api_key = AzKeyvault.AzureKeyVault.get_secret(self,"sagalabs-vpn-api-key")
        # Get public IP addresses from all the labs within the range
        public_ip_resources = VpnPublicIPAddresses().get(range_name)
        print(public_ip_resources)
        pass
