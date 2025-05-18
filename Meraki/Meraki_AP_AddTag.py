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
# Tagging Configuration
# ========================================
network_id = 'L_6xxx'  # TODO: Replace with actual network ID
tag_to_add = 'tag-to-add'  # TODO: Set desired tag
prefix = 'prefix'  # TODO: Set desired prefix
ssid_name = 'ssid'  # TODO: Set desired SSID name

print(f"Starting AP tagging for network {network_id}")
print(f"Tag: {tag_to_add}, Prefix: {prefix}, SSID: {ssid_name}")

# ========================================
# Execute AP Tagging
# ========================================
try:
    print("Getting network devices...")
    devices = dashboard.networks.getNetworkDevices(network_id)
    print(f"Found {len(devices)} devices")

    print("Getting network SSIDs...")
    ssids = dashboard.wireless.getNetworkWirelessSsids(network_id)
    print(f"Found {len(ssids)} SSIDs")

    print("Processing APs...")
    for device in devices:
        if 'MR' in device['model']:  # Check if the device is an AP
            if prefix in device['name']:
                device_serial = device['serial']
                tags = device.get('tags', [])
                
                if tag_to_add not in tags:
                    tags.append(tag_to_add)
                    dashboard.devices.updateDevice(device_serial, tags=tags)
                    print(f"Added tag '{tag_to_add}' to device {device['name']}")
                else:
                    print(f"Device {device['name']} already has tag '{tag_to_add}'")

    print("Updating SSID visibility...")
    for ssid in ssids:
        if ssid['name'] == ssid_name:
            ssid_number = ssid['number']
            dashboard.wireless.updateNetworkWirelessSsid(
                network_id,
                ssid_number,
                enabled=True,
                tags=[tag_to_add]
            )
            print(f"SSID '{ssid_name}' is now broadcasted by APs with tag '{tag_to_add}'")
            break
    else:
        print(f"SSID '{ssid_name}' not found")

    print("AP tagging completed successfully")
except Exception as e:
    print(f"Error during AP tagging: {e}")
    raise
