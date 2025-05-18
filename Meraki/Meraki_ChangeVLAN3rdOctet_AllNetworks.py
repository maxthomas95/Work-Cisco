import meraki
import csv
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import os

# Construct the path to the .env file
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
print(f"Loading .env file from: {env_path}")

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')

organization_id = os.getenv('ORGANIZATION_ID')

# Set up the Key Vault client
kv_uri = f"https://{key_vault_name}.vault.azure.net"

# Authenticate using ClientSecretCredential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)

# Retrieve the secret
API_KEY = client.get_secret(secret_name).value

# Initialize the Meraki API session
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# Get a list of all networks in the organization
networks = dashboard.organizations.getOrganizationNetworks(organization_id)

# Iterate through each network and update VLAN 1
for network in networks:
    network_id = network['id']
    try:
        # Get the current VLAN settings
        vlan = dashboard.appliance.getNetworkApplianceVlan(network_id, 1)

        # Modify the third octet of the VLAN subnet
        subnet_parts = vlan['subnet'].split('.')
        subnet_parts[2] = 'new_third_octet'  # Replace with the desired third octet
        new_subnet = '.'.join(subnet_parts)

        # Update the VLAN with the new subnet
        response = dashboard.appliance.updateNetworkApplianceVlan(
            network_id,
            1,
            subnet=new_subnet,
            applianceIp=new_subnet.replace('0/24', '1')  # Adjust the appliance IP accordingly
        )

        print(f"Updated VLAN 1 for network {network['name']}: {response}")
    except Exception as e:
        print(f"Failed to update VLAN 1 for network {network['name']}: {e}")