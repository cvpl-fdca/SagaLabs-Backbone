# api/vpn.py
import base64

from flask import jsonify
from flask_restx import Namespace, Resource, fields
import requests
from base64 import b64encode
from dotenv import load_dotenv
import os

from src.api.azure import VpnPublicIPAddresses
from src.tasks.azureTasks import get_resources
from src.utils import AzKeyVault
import atexit
import tempfile

load_dotenv()

vpn_ns = Namespace('vpn', description='vpn related operations')

API_KEY = AzKeyVault.AzKeyVault.get_secret("sagalabs-vpn-api-key")

# Generate the base64 encoded basic auth string
basic_auth_str = base64.b64encode("sagavpn-api:".encode() + API_KEY.encode()).decode()
HEADERS = {"Authorization": "Basic " + basic_auth_str, "Content-Type": "application/x-www-form-urlencoded"}


def handle_request(url, method='get', data=None):
    if method.lower() == 'get':
        response = requests.get(url, verify=False, headers=HEADERS)
    elif method.lower() == 'post':
        response = requests.post(url, verify=False, headers=HEADERS, data=data)
    return handle_response(response)


def handle_response(response):
    # If the status code is not 200, return an error message
    if response.status_code != 200:
        return {"error": f"HTTP error {response.status_code} received."}, response.status_code

    # If the status code is 200, check if the response is JSON
    try:
        json_response = response.json()
    except ValueError:
        # If the response is not JSON, return it as a string inside an object
        return {"message": response.text}, 200

    # If the response is JSON, return the JSON response
    return json_response, 200


@vpn_ns.route('/<string:range_name>/users')
class GetVPNUsers(Resource):

    def get(self, range_name):
        # Fetch the stored resources
        resources = get_resources()
        if not resources:
            return {"error": "No resources found"}, 500

        # Get the required range from the resources
        labs = resources.get(range_name)
        if not labs:
            return {"error": f"No labs found for range {range_name}"}, 404

        # Create a dict to store the results
        results = {range_name: {}}

        # For each lab in the range
        for lab_number, lab_resources in labs.items():
            # Extract IP addresses of the lab
            ip_addresses = [resource.get('ip_address') for resource in lab_resources if resource.get('ip_address')]

            # For each IP address, make a request to the VPN API and handle the response
            results[range_name][lab_number] = [handle_request(f"https://{ip}/api/users/list") for ip in ip_addresses]

        # Return the results
        return jsonify(results)


@vpn_ns.route('/<string:range_name>/<string:lab_number>/api/user/create')
class CreateVPNUserInSingleLab(Resource):
    @vpn_ns.expect(vpn_ns.model('CreateUser', {
        'username': fields.String(required=True, description='Username for the new VPN user'),
        'password': fields.String(default='', description='Password for the new VPN user (should be empty)'),
    }))
    def post(self, range_name, lab_number):
        payload = f"username={vpn_ns.payload['username']}"
        return handle_single_lab_request(range_name, lab_number, "/api/user/create", 'post', payload)


@vpn_ns.route('/<string:range_name>/<string:lab_number>/api/user/revoke')
class RevokeVPNUserInSingleLab(Resource):
    @vpn_ns.expect(vpn_ns.model('AlterUser', {
        'username': fields.String(required=True, description='Username for the VPN user'),
    }))
    def post(self, range_name, lab_number):
        payload = f"username={vpn_ns.payload['username']}"
        return handle_single_lab_request(range_name, lab_number, "/api/user/revoke", 'post', payload)

@vpn_ns.route('/<string:range_name>/<string:lab_number>/api/user/delete')
class DeleteVPNUserInSingleLab(Resource):
    @vpn_ns.expect(vpn_ns.model('AlterUser', {
        'username': fields.String(required=True, description='Username for the VPN user'),
    }))
    def post(self, range_name, lab_number):
        payload = f"username={vpn_ns.payload['username']}"
        return handle_single_lab_request(range_name, lab_number, "/api/user/delete", 'post', payload)


@vpn_ns.route('/<string:range_name>/user/create')
class CreateVPNUserInAllLabs(Resource):
    @vpn_ns.expect(vpn_ns.model('CreateUser', {
        'username': fields.String(required=True, description='Username for the new VPN user'),
        'password': fields.String(default='', description='Password for the new VPN user (should be empty)'),
    }))
    def post(self, range_name):
        return make_request_to_all_labs(range_name, "/api/user/create", 'post', vpn_ns.payload)


@vpn_ns.route('/<string:range_name>/user/revoke')
class RevokeVPNUserInAllLabs(Resource):
    @vpn_ns.expect(vpn_ns.model('AlterUser', {
        'username': fields.String(required=True, description='Username for the VPN user'),
    }))
    def post(self, range_name):
        return make_request_to_all_labs(range_name, "/api/user/revoke", 'post', vpn_ns.payload)


@vpn_ns.route('/<string:range_name>/user/delete')
class DeleteVPNUserInAllLabs(Resource):
    @vpn_ns.expect(vpn_ns.model('AlterUser', {
        'username': fields.String(required=True, description='Username for the VPN user'),
    }))
    def post(self, range_name):
        # First, revoke the user in all labs
        revoke_results = make_request_to_all_labs(range_name, "/api/user/revoke", 'post', vpn_ns.payload)

        # Then, delete the user in all labs
        delete_results = make_request_to_all_labs(range_name, "/api/user/delete", 'post', vpn_ns.payload)

        return {"revoke": revoke_results, "delete": delete_results}


def make_request_to_all_labs(range_name, url_path, method, data=None):
    # Fetch the stored resources
    resources = get_resources()
    if not resources:
        return {"error": "No resources found"}, 500

    # Get the required range from the resources
    labs = resources.get(range_name)
    if not labs:
        return {"error": f"No labs found for range {range_name}"}, 404

    results = {}  # Store the results for each lab

    # Iterate over all labs in the range
    for lab_number, lab_resources in labs.items():
        # Extract IP address of the lab
        ip_address = next((resource.get('ip_address') for resource in lab_resources if resource.get('ip_address')),
                          None)
        if not ip_address:
            results[lab_number] = {"error": f"No IP address found for lab {lab_number} in range {range_name}"}
            continue

        # Make a request to the VPN API and handle the response
        results[lab_number] = handle_request(f"https://{ip_address}{url_path}", method, data)

    return results


# A function to fetch the required range
def fetch_required_range(range_name):
    # Fetch the stored resources
    resources = get_resources()
    if not resources:
        return None, {"error": "No resources found"}, 500

    # Get the required range from the resources
    labs = resources.get(range_name)
    if not labs:
        return None, {"error": f"No labs found for range {range_name}"}, 404

    return labs, None, None


# A function to fetch the lab with a given number from a range
def fetch_lab_from_range(labs, lab_number):
    # Get the lab with the given lab number
    lab_resources = labs.get(lab_number)
    if not lab_resources:
        return None, {"error": f"No lab found with number {lab_number}"}, 404

    return lab_resources, None, None


# A function to extract the IP address from lab resources
def extract_ip_from_lab(lab_resources):
    # Extract IP address of the lab
    ip_address = next((resource.get('ip_address') for resource in lab_resources if resource.get('ip_address')), None)
    if not ip_address:
        return None, {"error": "No IP address found"}, 404

    return ip_address, None, None


# Function to handle single lab requests
def handle_single_lab_request(range_name, lab_number, url_path, method, data=None):
    labs, error, status = fetch_required_range(range_name)
    if error:
        return error, status

    lab_resources, error, status = fetch_lab_from_range(labs, lab_number)
    if error:
        return error, status

    ip_address, error, status = extract_ip_from_lab(lab_resources)
    if error:
        return error, status

    # Make a request to the VPN API and handle the response
    return handle_request(f"https://{ip_address}{url_path}", method, data)
