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

# Filter devices to only include MX models
mx_devices = [device for device in devices if device['model'].startswith('MX')]

# Get network names and second octet for each device
for device in mx_devices:
    if 'networkId' in device:
        network = dashboard.networks.getNetwork(device['networkId'])
        device['networkName'] = network['name']
    else:
        device['networkName'] = 'N/A'
    
    # Extract the second octet from the VLAN IP address
    if 'networkId' in device:
        try:
            vlan_id = '100'  # Replace with the actual VLAN ID if needed
            response = dashboard.appliance.getNetworkApplianceVlan(device['networkId'], vlan_id)
            appliance_ip = response['applianceIp']
            ip_parts = appliance_ip.split('.')
            if len(ip_parts) >= 2:
                device['secondOctet'] = int(ip_parts[1])  # Convert to integer for proper sorting
            else:
                device['secondOctet'] = -1  # Use -1 for invalid octets to sort them at the end
        except Exception as e:
            print(f"Error retrieving VLAN for device {device['serial']}: {e}")
            device['secondOctet'] = -1  # Use -1 for errors to sort them at the end
    else:
        device['secondOctet'] = -1  # Use -1 for missing networkId to sort them at the end

# Write devices information to a CSV file without duplicate network names and sorted by Second Octet
def write_to_csv(devices, folder_path='Python_Scripts/Meraki/Output'):
    seen_network_names = set()
    unique_devices = []
    
    for device in devices:
        if device['networkName'] not in seen_network_names:
            unique_devices.append(device)
            seen_network_names.add(device['networkName'])
    
    # Sort devices by Second Octet (numerically)
    unique_devices.sort(key=lambda x: x['secondOctet'])
    
    # Ensure the folder path exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Define the CSV file name and path
    csv_file_name = 'mx_devices.csv'
    csv_file_path = os.path.join(folder_path, csv_file_name)
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Network Name', 'Network ID', 'Second Octet'])
        for device in unique_devices:
            writer.writerow([device['networkName'], device.get('networkId', ''), device['secondOctet']])

# Write MX devices to CSV
write_to_csv(mx_devices)

print(f"MX devices information with unique network names and second octet has been successfully written to Python_Scripts/Meraki/Output/mx_devices.csv")