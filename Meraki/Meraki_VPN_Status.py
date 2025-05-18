import os
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
# Check VPN Statuses
# ========================================
try:
    print(f"Checking VPN statuses for organization {organization_id}")
    vpn_statuses = dashboard.appliance.getOrganizationApplianceVpnStatuses(organization_id)
    
    print("\nVPN Status Summary:")
    print("=" * 40)
    for status in vpn_statuses:
        network_name = status.get('networkName', 'Unknown')
        device_count = len(status.get('devices', []))
        print(f"Network: {network_name}")
        print(f"Devices: {device_count}")
        for device in status.get('devices', []):
            print(f"  - {device.get('name')}: {'Active' if device.get('connectionStatus') == 'active' else 'Inactive'}")
        print("-" * 40)
        
except Exception as e:
    print(f"Error checking VPN statuses: {e}")
    raise
