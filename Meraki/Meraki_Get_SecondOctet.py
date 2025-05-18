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
# VLAN Configuration
# ========================================
network_id = 'L_xxxx'  # TODO: Set target network ID
vlan_id = '100'  # TODO: Set target VLAN ID

try:
    print(f"Getting VLAN {vlan_id} configuration from network {network_id}")
    vlan = dashboard.appliance.getNetworkApplianceVlan(network_id, vlan_id)
    
    appliance_ip = vlan['applianceIp']
    second_octet = appliance_ip.split('.')[1]
    
    print("\nVLAN Details:")
    print(f"- Appliance IP: {appliance_ip}")
    print(f"- Second Octet: {second_octet}")
    print(f"- VLAN Name: {vlan.get('name', 'N/A')}")
    print(f"- Subnet: {vlan.get('subnet', 'N/A')}")
    
except Exception as e:
    print(f"[ERROR] Failed to get VLAN configuration: {e}")
    raise
