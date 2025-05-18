import meraki
import csv
import os

CSV_FILE = 'ict_ports.csv'

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
key_vault_name = os.getenv('AZURE_KEY_VAULT')

# Set up the Key Vault client
kv_uri = f"https://{key_vault_name}.vault.azure.net"

# Authenticate using ClientSecretCredential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)

# Retrieve the secret
secret_name = "Meraki-API"
API_KEY = client.get_secret(secret_name).value

# Initialize the Meraki API session
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# Function to find ports labeled "ICT" and save to CSV
def find_ict_ports(api_key, csv_file):
    try:
        # Open CSV file for writing
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Network Name', 'Device Name', 'Device Model', 'Port ID', 'Port Name'])

            # Get the list of organizations
            organizations = dashboard.organizations.getOrganizations()
            
            for org in organizations:
                org_id = org['id']
                
                # Get the list of networks in the organization
                networks = dashboard.organizations.getOrganizationNetworks(org_id)
                
                for network in networks:
                    network_id = network['id']
                    network_name = network['name']
                    
                    # Get the list of devices in the network
                    devices = dashboard.networks.getNetworkDevices(network_id)
                    
                    for device in devices:
                        # Check if the device is an MS switch
                        if 'MS' in device['model']:
                            print(f"Checking ports on MS device: {device['name']} (Model: {device['model']}) in network {network_name}")
                            
                            # Get the list of switch ports for each MS device
                            ports = dashboard.switch.getDeviceSwitchPorts(device['serial'])
                            
                            for port in ports:
                                # Check if the port name exists and contains "ICT"
                                if port.get('name') and 'ICT' in port['name']:
                                    writer.writerow([network_name, device['name'], device['model'], port['portId'], port['name']])
                                    print(f"Found ICT port: {port['name']} on device {device['name']} (Port ID: {port['portId']}) in network {network_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Find ICT ports and save to CSV
find_ict_ports(API_KEY, CSV_FILE)
