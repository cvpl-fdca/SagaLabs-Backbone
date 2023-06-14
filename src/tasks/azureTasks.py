import json
from apscheduler.schedulers.background import BackgroundScheduler
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.network import NetworkManagementClient
from dotenv import load_dotenv
import os
import redis

load_dotenv()

# Authenticate to Azure
credential = DefaultAzureCredential()

# Create a client for the compute service
compute_client = ComputeManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_ID"))
resource_client = ResourceManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_ID"))
network_client = NetworkManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_ID"))

# Instantiate Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
if redis_host != "redis":
    print("Redis host environment variable not set. Meaby we are developing and this isnt running in docker? "
          "Defaulting to: " + redis_host)
r = redis.Redis(host=redis_host, port=6379, db=0)


def poll_resources():
    resources_dict = {}
    print(redis_host)
    for resource_group in resource_client.resource_groups.list():
        try:
            if resource_group.tags and resource_group.tags.get('lab') == 'true':
                resources_in_group = resource_client.resources.list_by_resource_group(resource_group.name)

                range_name = resource_group.tags.get('range')
                lab_number = resource_group.tags.get('lab_number')

                if range_name and lab_number:
                    if range_name not in resources_dict:
                        resources_dict[range_name] = {}

                    # convert each resource to a dictionary
                    resources_in_group = [res.serialize(True) for res in resources_in_group]

                    # Fetch the IP address of Public IP Address resources
                    for resource in resources_in_group:
                        if resource['type'] == 'Microsoft.Network/publicIPAddresses':
                            public_ip = network_client.public_ip_addresses.get(resource_group.name, resource['name'])
                            resource['ip_address'] = public_ip.ip_address

                    resources_dict[range_name][lab_number] = resources_in_group
        except ResourceNotFoundError:
            print(f"Resource group {resource_group.name} not found.")

    # Store the resources in Redis
    r.set('RESOURCES', json.dumps(resources_dict))

    print(f"Updated resources: {len(resources_dict)}")


scheduler = BackgroundScheduler()
scheduler.add_job(poll_resources, 'interval', minutes=1)
scheduler.start()


def get_resources():
    # Fetch resources from Redis
    resources = json.loads(r.get('RESOURCES') or '{}')
    return resources
