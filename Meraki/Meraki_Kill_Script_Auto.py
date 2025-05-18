import csv
from difflib import get_close_matches
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

def get_network_id_from_csv(csv_file_path, name):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        names = [row['Name'] for row in csv_reader]
        # Find close matches to the given name
        close_matches = get_close_matches(name, names, n=5, cutoff=0.4)  # Set cutoff to 0.0 to suggest even weak matches
        if close_matches:
            print("Did you mean one of the following?")
            for i, match in enumerate(close_matches, 1):
                print(f"{i}. {match}")
            selected = int(input("Enter the number of the correct device name, or 0 if none: "))
            if selected > 0:
                # Reset file pointer to the beginning
                file.seek(0)
                # If user selects a match, find the network ID for the selected match
                for row in csv_reader:
                    if row['Name'] == close_matches[selected - 1]:
                        return row['Network ID']
        else:
            # If no close matches, return None
            return None

# Define the folder path and CSV file name
folder_path = 'Python_Scripts/Meraki/Output'
csv_file_name = os.path.join(folder_path, 'devices.csv')

# Set the path to your CSV file
CSV_FILE_PATH = csv_file_name

print(f"CSV file path: {CSV_FILE_PATH}")
# Prompt the user for the device name
name_to_search = input("Please enter the device name: ")

# Get the network ID using the provided name
network_id = get_network_id_from_csv(CSV_FILE_PATH, name_to_search)

if network_id:
    print(f"The Network ID for {name_to_search} is {network_id}.")
else:
    print(f"No Network ID found for the name {name_to_search}.")

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
        {'hubId': 'N_xxxx1', 'useDefaultRoute': True},
        {'hubId': 'N_6xxxx', 'useDefaultRoute': True}
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


