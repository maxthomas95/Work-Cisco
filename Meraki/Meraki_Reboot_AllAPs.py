import meraki
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

def get_organization_devices(org_id):
    """Retrieve all devices in the given organization."""
    try:
        devices = dashboard.organizations.getOrganizationDevices(org_id)
        return devices
    except meraki.APIError as e:
        print(f"Meraki API Error: {e}")
    except Exception as e:
        print(f"Error retrieving devices: {e}")
    return []

def reboot_all_aps(org_id):
    """Reboot all access points (APs) in the organization."""
    devices = get_organization_devices(org_id)
    
    if not devices:
        print("No devices found in the organization.")
        return

    aps = [device for device in devices if device['model'].startswith('MR')]  # MR = Meraki APs

    if not aps:
        print("No access points found.")
        return

    print(f"Found {len(aps)} APs. Rebooting...")

    for ap in aps:
        try:
            dashboard.devices.rebootDevice(ap['serial'])
            print(f"Rebooted AP: {ap['name']} (Serial: {ap['serial']})")
        except meraki.APIError as e:
            print(f"Failed to reboot {ap['name']} (Serial: {ap['serial']}): {e}")
        except Exception as e:
            print(f"Unexpected error on {ap['name']} (Serial: {ap['serial']}): {e}")

# Run the script
if __name__ == "__main__":
    reboot_all_aps(organization_id)
