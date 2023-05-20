from azure.identity import DefaultAzureCredential
from flask_restx import Namespace, Resource
from ..tasks.azure_tasks import get_resources
from azure.mgmt.compute import ComputeManagementClient
from dotenv import load_dotenv
import os

load_dotenv()

# Authenticate to Azure
credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_ID"))

azure_ns = Namespace('azure', description='Azure related operations')


# endpoint for getting all ranges
@azure_ns.route('/ranges')
class Ranges(Resource):
    def get(self):
        # Assuming `resources` is a global list where you store your resources
        # from the task scheduler, you can simply return it here.
        # If it's not a global variable, you'll need to provide a way
        # to access it from this method.
        return get_resources(), 200


@azure_ns.route('/<string:range_name>')
class Range(Resource):
    def get(self, range_name):
        # get all resources
        all_resources = get_resources()

        # get the specific range
        range_resources = all_resources.get(range_name)

        if range_resources is None:
            # if the range_id does not exist, return a 404 error
            azure_ns.abort(404, f"Range {range_name} not found.")
        else:
            # return the specific range
            return range_resources, 200


@azure_ns.route('/<string:range_name>/<string:lab_number>')
class Lab(Resource):
    def get(self, range_name, lab_number):
        # get all resources
        all_resources = get_resources()

        # get the specific range
        range_resources = all_resources.get(range_name)

        if range_resources is None:
            # if the range_id does not exist, return a 404 error
            azure_ns.abort(404, f"Range {range_name} not found.")

        # get the specific lab
        lab_resources = range_resources.get(lab_number)

        if lab_resources is None:
            # if the lab_number does not exist, return a 404 error
            azure_ns.abort(404, f"Lab {lab_number} not found in Range {range_name}.")
        else:
            # return the specific lab
            return lab_resources, 200


@azure_ns.route('/<string:range_name>/vpn')
class PublicIPAddresses(Resource):
    def get(self, range_name):
        # get all resources
        all_resources = get_resources()

        # get the specific range
        range_resources = all_resources.get(range_name)

        if range_resources is None:
            # if the range_name does not exist, return a 404 error
            azure_ns.abort(404, f"Range {range_name} not found.")

        # iterate through all labs within the range, and for each lab, find all resources of the type
        # "Microsoft.Network/publicIPAddresses"
        public_ip_resources = {}
        for lab_number, lab_resources in range_resources.items():
            for resource in lab_resources:
                if resource['type'] == 'Microsoft.Network/publicIPAddresses':
                    if lab_number not in public_ip_resources:
                        public_ip_resources[lab_number] = []
                    public_ip_resources[lab_number].append(resource)

        # return the dictionary of public IP address resources grouped by lab numbers
        return public_ip_resources, 200


@azure_ns.route('/<string:range_name>/<string:lab_number>/vpn')
class LabPublicIPAddresses(Resource):
    def get(self, range_name, lab_number):
        # get all resources
        all_resources = get_resources()

        # get the specific range
        range_resources = all_resources.get(range_name)

        if range_resources is None:
            # if the range_name does not exist, return a 404 error
            azure_ns.abort(404, f"Range {range_name} not found.")

        # get the specific lab
        lab_resources = range_resources.get(lab_number)

        if lab_resources is None:
            # if the lab_number does not exist, return a 404 error
            azure_ns.abort(404, f"Lab {lab_number} in range {range_name} not found.")

        # iterate through resources in the lab, find all resources of the type
        # "Microsoft.Network/publicIPAddresses"
        public_ip_resources = []
        for resource in lab_resources:
            if resource['type'] == 'Microsoft.Network/publicIPAddresses':
                public_ip_resources.append(resource)

        # return the list of public IP address resources
        return public_ip_resources, 200


@azure_ns.route('/<string:range_name>/<string:lab_number>/set/disks/slow')
class SetDisksFast(Resource):
    def post(self, range_name, lab_number):
        # Get all resources
        all_resources = get_resources()

        # Get the specific range and lab
        range_resources = all_resources.get(range_name)
        lab_resources = range_resources.get(lab_number) if range_resources else None

        if lab_resources is None:
            # If the range_name or lab_number does not exist, return a 404 error
            azure_ns.abort(404, f"Range {range_name} or lab {lab_number} not found.")

        # Iterate through all resources in the lab and set the disks to Standard HDD
        for resource in lab_resources:
            if resource['type'] == 'Microsoft.Compute/disks':
                # Extract resource group from disk's ID
                resource_group_name = resource['id'].split('/')[4]
                disk_name = resource['name']

                # Get the disk
                disk = compute_client.disks.get(resource_group_name=resource_group_name, disk_name=disk_name)

                # Update disk SKU
                disk.sku.name = 'Standard_LRS'  # Set the disk to Standard HDD

                # Update the disk
                compute_client.disks.begin_create_or_update(resource_group_name, disk_name, disk)

        return {"message": "All disks have been set to Standard HDD."}, 200


@azure_ns.route('/<string:range_name>/<string:lab_number>/set/disks/fast')
class SetDisksFast(Resource):
    def post(self, range_name, lab_number):
        # Get all resources
        all_resources = get_resources()

        # Get the specific range and lab
        range_resources = all_resources.get(range_name)
        lab_resources = range_resources.get(lab_number) if range_resources else None

        if lab_resources is None:
            # If the range_name or lab_number does not exist, return a 404 error
            azure_ns.abort(404, f"Range {range_name} or lab {lab_number} not found.")

        # Iterate through all resources in the lab and set the disks to Premium SSD
        for resource in lab_resources:
            if resource['type'] == 'Microsoft.Compute/disks':
                # Extract resource group from disk's ID
                resource_group_name = resource['id'].split('/')[4]
                disk_name = resource['name']

                # Get the disk
                disk = compute_client.disks.get(resource_group_name=resource_group_name, disk_name=disk_name)

                # Update disk SKU
                disk.sku.name = 'Premium_LRS'  # Set the disk to Premium SSD

                # Update the disk
                compute_client.disks.begin_create_or_update(resource_group_name, disk_name, disk)

        return {"message": "All disks have been set to Premium SSD."}, 200


@azure_ns.route('/<string:range_name>/start')
class StartVmsInRange(Resource):
    def post(self, range_name):
        # get all resources
        all_resources = get_resources()

        # get the specific range
        range_resources = all_resources.get(range_name)

        if range_resources is None:
            # if the range_id does not exist, return a 404 error
            azure_ns.abort(404, f"Range {range_name} not found.")

        dc_started = False
        # iterate through all labs within the range, and for each lab, find all resources of the type
        # "Microsoft.Compute/virtualMachines"
        for lab_number, lab_resources in range_resources.items():
            for resource in lab_resources:
                if resource['type'] == 'Microsoft.Compute/virtualMachines':
                    # Extract resource group from VM's ID
                    resource_group_name = resource['id'].split('/')[4]
                    vm_name = resource['name']

                    if 'DC' in vm_name:
                        # Start the DC VM first
                        compute_client.virtual_machines.begin_start(resource_group_name, vm_name)
                        dc_started = True

        if not dc_started:
            azure_ns.abort(400, f"No Domain Controller found in Range {range_name}.")

        # start other VMs
        for lab_number, lab_resources in range_resources.items():
            for resource in lab_resources:
                if resource['type'] == 'Microsoft.Compute/virtualMachines':
                    resource_group_name = resource['id'].split('/')[4]
                    vm_name = resource['name']

                    if 'DC' not in vm_name:
                        # Start the non-DC VM
                        compute_client.virtual_machines.begin_start(resource_group_name, vm_name)

        return {"message": f"All virtual machines in Range {range_name} are being started."}, 200


@azure_ns.route('/<string:range_name>/stop')
class StopVmsInRange(Resource):
    def post(self, range_name):
        # get all resources
        all_resources = get_resources()

        # get the specific range
        range_resources = all_resources.get(range_name)

        if range_resources is None:
            # if the range_id does not exist, return a 404 error
            azure_ns.abort(404, f"Range {range_name} not found.")

        dc_name = None
        dc_resource_group = None

        # stop non-DC VMs first
        for lab_number, lab_resources in range_resources.items():
            for resource in lab_resources:
                if resource['type'] == 'Microsoft.Compute/virtualMachines':
                    resource_group_name = resource['id'].split('/')[4]
                    vm_name = resource['name']

                    if 'DC' in vm_name:
                        # Save the DC details for stopping later
                        dc_name = vm_name
                        dc_resource_group = resource_group_name
                    else:
                        # Stop the non-DC VM
                        compute_client.virtual_machines.begin_deallocate(resource_group_name, vm_name)

        if dc_name is None or dc_resource_group is None:
            azure_ns.abort(400, f"No Domain Controller found in Range {range_name}.")

        # Stop the DC VM last
        compute_client.virtual_machines.begin_deallocate(dc_resource_group, dc_name)

        return {"message": f"All virtual machines in Range {range_name} are being stopped."}, 200
