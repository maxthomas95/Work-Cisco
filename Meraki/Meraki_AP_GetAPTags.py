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

# Set up the Key Vault client
kv_uri = f"https://{key_vault_name}.vault.azure.net"

# Authenticate using ClientSecretCredential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)

# Retrieve the secret
API_KEY = client.get_secret(secret_name).value

# Initialize the Meraki API session
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

network_id = 'N_577586652210280116'

# Get the list of devices in the network
devices = dashboard.networks.getNetworkDevices(network_id)

# Initialize a list to store the results
ap_info = []

# Iterate through each device to get tags
for device in devices:
    if 'MR' in device['model']:  # Check if the device is an AP
        device_serial = device['serial']
        tags = device.get('tags', [])
        
        ap_info.append({
            'device_name': device['name'],
            'serial': device_serial,
            'model': device['model'],
            'tags': tags
        })

# Define the CSV file name
csv_file = 'ap_tags.csv'

# Write the response to a CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['device_name', 'serial', 'model', 'tags'])
    writer.writeheader()
    for ap in ap_info:
        writer.writerow({
            'device_name': ap['device_name'],
            'serial': ap['serial'],
            'model': ap['model'],
            'tags': ', '.join(ap['tags'])
        })

print(f"Data has been written to {csv_file}")
