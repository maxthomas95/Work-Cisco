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
network_id = 'L_xxx'  # TODO: Replace with actual network ID
vlan_id = 1  # TODO: Set desired VLAN ID
new_third_octet = 'xxx'  # TODO: Set desired third octet value

print(f"Preparing to update VLAN {vlan_id} on network {network_id}")
print(f"Will modify third octet to: {new_third_octet}")

# ========================================
# Execute VLAN Update
# ========================================
try:
    print("Getting current VLAN settings...")
    vlan = dashboard.appliance.getNetworkApplianceVlan(network_id, vlan_id)
    
    # Modify the third octet of the VLAN subnet
    subnet_parts = vlan['subnet'].split('.')
    subnet_parts[2] = new_third_octet
    new_subnet = '.'.join(subnet_parts)
    print(f"New subnet will be: {new_subnet}")

    print("Updating VLAN configuration...")
    response = dashboard.appliance.updateNetworkApplianceVlan(
        network_id,
        vlan_id,
        subnet=new_subnet,
        applianceIp=new_subnet.replace('0/24', '1')  # Adjust the appliance IP accordingly
    )
    print(f"Successfully updated VLAN {vlan_id}: {response}")

except Exception as e:
    print(f"Error updating VLAN: {e}")
    raise
