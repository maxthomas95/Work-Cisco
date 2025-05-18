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
# Device Management Functions
# ========================================
def get_organization_devices(org_id):
    """Retrieve all devices in the given organization."""
    try:
        print(f"Getting devices for organization {org_id}")
        devices = dashboard.organizations.getOrganizationDevices(org_id)
        print(f"Found {len(devices)} total devices")
        return devices
    except Exception as e:
        print(f"[ERROR] Failed to get devices: {e}")
        raise

def reboot_all_aps(org_id):
    """Reboot all access points (APs) in the organization."""
    try:
        devices = get_organization_devices(org_id)
        if not devices:
            raise ValueError("No devices found in organization")
        
        aps = [d for d in devices if d.get('model', '').startswith('MR')]
        if not aps:
            raise ValueError("No Meraki APs (MR models) found")
            
        print(f"\nFound {len(aps)} APs to reboot:")
        for ap in aps:
            print(f"- {ap.get('name', 'Unnamed')} ({ap.get('serial', 'Unknown')})")
            
        confirm = input("\nConfirm reboot of all APs? (y/n): ")
        if confirm.lower() != 'y':
            print("Reboot cancelled")
            return
            
        print("\nRebooting APs...")
        for ap in aps:
            try:
                dashboard.devices.rebootDevice(ap['serial'])
                print(f"Rebooted: {ap.get('name', 'Unnamed')} ({ap.get('serial', 'Unknown')})")
            except Exception as e:
                print(f"[WARNING] Failed to reboot {ap.get('name', 'Unnamed')}: {e}")
                
        print("\nAP reboot process completed")
        
    except Exception as e:
        print(f"[ERROR] AP reboot failed: {e}")
        raise

# ========================================
# Main Execution
# ========================================
if __name__ == "__main__":
    reboot_all_aps(organization_id)
