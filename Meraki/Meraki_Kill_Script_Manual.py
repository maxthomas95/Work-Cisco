import meraki
import time

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

network_id = ""
wait_time = 30

# Get a list of all VLANs in the network
vlans = dashboard.appliance.getNetworkApplianceVlans(network_id)

# Iterate through each VLAN and update DHCP handling
for vlan in vlans:
    vlan_id = vlan['id']
    response = dashboard.appliance.updateNetworkApplianceVlan(
        network_id, vlan_id,
        dhcpHandling='Do not respond to DHCP requests'
    )
    print(f"Updated VLAN {vlan_id}: {response}")

# Set 'mode' to none, for VPN
mode = 'none'
response = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
    network_id, mode,
)
print(response)

#Wait for x seconds
time.sleep(wait_time)

# Set 'mode' to spoke, for VPN. Add both hubs back
mode = 'spoke'
response = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
    network_id, mode,
    hubs=[
        {'hubId': 'N_xxxx', 'useDefaultRoute': True},
        {'hubId': 'N_xxxx', 'useDefaultRoute': True}
    ]
)
print(response)

# Iterate through each VLAN and update DHCP handling and relay settings
for vlan in vlans:
    vlan_id = vlan['id']
    response = dashboard.appliance.updateNetworkApplianceVlan(
        network_id, vlan_id,
        dhcpHandling='Relay DHCP to another server',
        dhcpRelayServerIps=['1.1.1.1', '8.8.8.8']
    )
    print(f"Updated VLAN {vlan_id}: {response}")