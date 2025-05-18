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


# Get all devices in the organization
devices = dashboard.organizations.getOrganizationDevices(organization_id)

# Filter for MX devices and prepare their public IP addresses for CSV output
mx_devices_public_ips = [
    {'Device Name': device['name'], 'WAN1 IP': device['wan1Ip'], 'WAN2 IP': device['wan2Ip']}
    for device in devices if 'MX' in device['model']
]

# Define the folder path and CSV file name
folder_path = 'Python_Scripts/Meraki/Output'
csv_file_name = os.path.join(folder_path, 'mx_devices_public_ips.csv')

# Write the results to a CSV file
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Device Name', 'WAN1 IP', 'WAN2 IP'])
    writer.writeheader()
    writer.writerows(mx_devices_public_ips)

# Print a success message
print(f"MX devices' public IP addresses have been successfully written to {csv_file_name}.")
