import os
import csv
import meraki
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

# ========================================
# Load secrets from .env
# ========================================
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
print(f"Loading .env file from: {env_path}")
load_dotenv(dotenv_path=env_path)

organization_id = os.getenv('ORGANIZATION_ID')
tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
key_vault_name = os.getenv('AZURE_KEY_VAULT')
meraki_secret_name = os.getenv('MERAKI_SECRET_NAME')

# ========================================
# Authenticate to Azure Key Vault
# ========================================
kv_uri = f"https://{key_vault_name}.vault.azure.net"
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)
API_KEY = client.get_secret(meraki_secret_name).value

# ========================================
# Connect to Meraki Dashboard API
# ========================================
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# ========================================
# Output Configuration
# ========================================
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'Output')
os.makedirs(output_dir, exist_ok=True)
CSV_FILE = os.path.join(output_dir, 'camera_ports.csv')

# ========================================
# Find Camera Ports Function
# ========================================
def find_camera_ports(api_key, csv_file):
    try:
        print(f"Starting camera port search across organization {organization_id}")
        
        # Open CSV file for writing
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Network Name', 'Device Name', 'Device Model', 'Port ID', 'Port Name'])

            # Get the list of networks in the organization
            networks = dashboard.organizations.getOrganizationNetworks(organization_id)
            print(f"Found {len(networks)} networks to scan for camera ports")
            
            for network in networks:
                network_id = network['id']
                network_name = network['name']
                print(f"Scanning network: {network_name}")
                
                # Get the list of devices in the network
                devices = dashboard.networks.getNetworkDevices(network_id)
                
                for device in devices:
                    # Check if the device is an MS switch
                    if 'MS' in device['model']:
                        print(f"Checking ports on MS device: {device['name']} (Model: {device['model']})")
                        
                        # Get the list of switch ports for each MS device
                        ports = dashboard.switch.getDeviceSwitchPorts(device['serial'])
                        
                        for port in ports:
                                # Check if the port name exists and contains "Camera"
                                if port.get('name') and 'Camera' in port['name']:
                                    writer.writerow([network_name, device['name'], device['model'], port['portId'], port['name']])
                                    print(f"Found camera port: {port['name']} on device {device['name']} (Port ID: {port['portId']})")
    except Exception as e:
        print(f"Error during camera port search: {e}")
        raise

# ========================================
# Execute ICT Port Search
# ========================================
print(f"Starting camera port tracking...")
find_camera_ports(API_KEY, CSV_FILE)
