import json
from apscheduler.schedulers.background import BackgroundScheduler
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.network import NetworkManagementClient
from dotenv import load_dotenv
import os
load_dotenv()

# Authenticate to Azure
credential = DefaultAzureCredential()

# Create a client for the compute service
compute_client = ComputeManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_ID"))
resource_client = ResourceManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_ID"))
network_client = NetworkManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_ID"))

# This is where you'll store the resources
RESOURCES = ["not pulled from azure yet. wait a couple minutes for me to start up"]


def poll_resources():
    global RESOURCES
    RESOURCES = {}

    for resource_group in resource_client.resource_groups.list():
        try:
            if resource_group.tags and resource_group.tags.get('lab') == 'true':
                resources_in_group = resource_client.resources.list_by_resource_group(resource_group.name)

                range_name = resource_group.tags.get('range')
                lab_number = resource_group.tags.get('lab_number')

                if range_name and lab_number:
                    if range_name not in RESOURCES:
                        RESOURCES[range_name] = {}

                    # convert each resource to a dictionary
                    resources_in_group = [res.serialize(True) for res in resources_in_group]

                    # Fetch the IP address of Public IP Address resources
                    for resource in resources_in_group:
                        if resource['type'] == 'Microsoft.Network/publicIPAddresses':
                            public_ip = network_client.public_ip_addresses.get(resource_group.name, resource['name'])
                            resource['ip_address'] = public_ip.ip_address

                    RESOURCES[range_name][lab_number] = resources_in_group
        except ResourceNotFoundError:
            print(f"Resource group {resource_group.name} not found.")

    print(f"Updated resources: {len(RESOURCES)}")


scheduler = BackgroundScheduler()
scheduler.add_job(poll_resources, 'interval', minutes=1)
scheduler.start()


def get_resources():
    global RESOURCES
    return RESOURCES
