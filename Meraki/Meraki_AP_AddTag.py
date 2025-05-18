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

# Set up the Key Vault client
kv_uri = f"https://{key_vault_name}.vault.azure.net"

# Authenticate using ClientSecretCredential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)

# Retrieve the secret
API_KEY = client.get_secret(secret_name).value

# Initialize the Meraki API session
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

network_id = 'L_6xxx'
tag_to_add = 'tag-to-add'
prefix = 'prefix'  # Change this variable to the desired prefix
ssid_name = 'ssid'  # Change this variable to the desired SSID name

# Get the list of devices in the network
devices = dashboard.networks.getNetworkDevices(network_id)

# Get the SSIDs for the network
ssids = dashboard.wireless.getNetworkWirelessSsids(network_id)

# Iterate through each device to check the name and add the tag if necessary
for device in devices:
    if 'MR' in device['model']:  # Check if the device is an AP
        if prefix in device['name']:
            device_serial = device['serial']
            tags = device.get('tags', [])
            
            # Add the tag if it's not already present
            if tag_to_add not in tags:
                tags.append(tag_to_add)
                dashboard.devices.updateDevice(device_serial, tags=tags)
                print(f"Added tag '{tag_to_add}' to device {device['name']}")

# Ensure the SSID is broadcasted by the APs with the tag
for ssid in ssids:
    if ssid['name'] == ssid_name:
        ssid_number = ssid['number']
        dashboard.wireless.updateNetworkWirelessSsid(
            network_id,
            ssid_number,
            enabled=True,
            tags=[tag_to_add]
        )
        print(f"SSID '{ssid_name}' is now broadcasted by APs with the tag '{tag_to_add}'")
