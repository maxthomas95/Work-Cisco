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
csv_file = os.path.join(output_dir, 'ap_tags.csv')

# ========================================
# Get AP Tags
# ========================================
try:
    network_id = 'N_xxxx'  # TODO: Replace with actual network ID
    print(f"Getting AP tags for network {network_id}")
    
    # Get the list of devices in the network
    devices = dashboard.networks.getNetworkDevices(network_id)
    print(f"Found {len(devices)} devices")

    # Initialize a list to store the results
    ap_info = []
    ap_count = 0

    # Iterate through each device to get tags
    for device in devices:
        if 'MR' in device['model']:  # Check if the device is an AP
            ap_count += 1
            device_serial = device['serial']
            tags = device.get('tags', [])
            
            ap_info.append({
                'device_name': device['name'],
                'serial': device_serial,
                'model': device['model'],
                'tags': tags
            })
            print(f"Processed AP: {device['name']} with {len(tags)} tags")

    print(f"Found {ap_count} APs with tags")

    # Write the response to a CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['device_name', 'serial', 'model', 'tags'])
        writer.writeheader()
        for ap in ap_info:
            writer.writerow({
                'device_name': ap['device_name'],
                'serial': ap['serial'],
                'model': ap['model'],
                'tags': ', '.join(ap['tags']) if ap['tags'] else 'None'
            })
        print(f"AP tag data successfully written to {csv_file}")

except Exception as e:
    print(f"Error getting AP tags: {e}")
    raise
