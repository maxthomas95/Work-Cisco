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

# Function to find client devices with a specific IP and save to CSV
def find_client_ips(api_key, csv_file, target_ip):
    try:
        # Open CSV file for writing
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Network Name', 'Client Description', 'Client MAC', 'Client IP', 'Device Name', 'Device Model'])

            # Get the list of organizations
            organizations = dashboard.organizations.getOrganizations()
            print(f"Found {len(organizations)} organizations.")
            
            for org in organizations:
                org_id = org['id']
                
                # Get the list of networks in the organization
                networks = dashboard.organizations.getOrganizationNetworks(org_id)
                print(f"Found {len(networks)} networks in organization {org_id}.")
                
                for network in networks:
                    network_id = network['id']
                    network_name = network['name']
                    
                    # Get the list of clients in the network
                    clients = dashboard.networks.getNetworkClients(network_id, timespan=604800)  # Last 7 days
                    print(f"Found {len(clients)} clients in network {network_name}.")
                    
                    for client in clients:
                        # Check if the client IP matches the target IP
                        client_ip = client.get('ip') or client.get('recentDeviceIp')
                        if client_ip == target_ip:
                            device_serial = client.get('recentDeviceSerial')
                            if device_serial:
                                device = dashboard.devices.getDevice(device_serial)
                                writer.writerow([network_name, client.get('description', 'N/A'), client['mac'], client_ip, device['name'], device['model']])
                                print(f"Found client with IP {target_ip}: {client_ip} on device {device['name']} in network {network_name}")
                            else:
                                print(f"Client with IP {target_ip} found, but no device serial: {client_ip}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage: Find client devices with a specific IP and save to CSV
target_ip = '192.168.128.6'  # Replace with the IP address you want to search for
CSV_FILE = 'found_ips.csv'
find_client_ips(API_KEY, CSV_FILE, target_ip)
