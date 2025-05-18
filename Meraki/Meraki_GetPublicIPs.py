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
# Get MX Devices Public IPs
# ========================================
try:
    print(f"Getting all devices for organization {organization_id}")
    devices = dashboard.organizations.getOrganizationDevices(organization_id)
    
    mx_devices = [device for device in devices if 'MX' in device.get('model', '')]
    print(f"Found {len(mx_devices)} MX devices with public IPs")

    mx_public_ips = []
    for device in mx_devices:
        mx_public_ips.append({
            'Device Name': device.get('name', 'N/A'),
            'WAN1 IP': device.get('wan1Ip', 'N/A'),
            'WAN2 IP': device.get('wan2Ip', 'N/A')
        })

# ========================================
# CSV Output Configuration
# ========================================
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'Output')
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'mx_public_ips.csv')

    with open(csv_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Device Name', 'WAN1 IP', 'WAN2 IP'])
        writer.writeheader()
        writer.writerows(mx_public_ips)

    print(f"\nSuccessfully wrote public IPs for {len(mx_public_ips)} MX devices to {csv_path}")

except Exception as e:
    print(f"[ERROR] Failed to get public IPs: {e}")
    raise
