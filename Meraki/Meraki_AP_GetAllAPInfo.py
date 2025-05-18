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
csv_file = os.path.join(output_dir, 'network_wireless_ssids.csv')

# ========================================
# Get Wireless SSIDs
# ========================================
try:
    network_id = 'N_xxxx'  # TODO: Replace with actual network ID
    print(f"Getting wireless SSIDs for network {network_id}")
    
    response = dashboard.wireless.getNetworkWirelessSsids(network_id)
    print(f"Found {len(response)} SSIDs")

    # Collect all unique keys from the response
    keys = set()
    for ssid in response:
        keys.update(ssid.keys())

    # Write the response to a CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(response)
        print(f"SSID data successfully written to {csv_file}")

except Exception as e:
    print(f"Error getting wireless SSIDs: {e}")
    raise
