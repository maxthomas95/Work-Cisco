import meraki
import csv
import os
import time
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

# Construct the path to the .env file
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
print(f"Loading .env file from: {env_path}")

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')

# Set up the Key Vault client


# Authenticate using ClientSecretCredential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)

# Retrieve the secret
API_KEY = client.get_secret(secret_name).value

# Initialize the Meraki API session
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# Function to check if the third octet is 251
def is_matching_ip(ip):
    if ip is None:
        return False
    parts = ip.split('.')
    return len(parts) == 4 and parts[2] == '251'

# Function to disable switch ports
def disable_ports(ports):
    for serial, port in ports:
        dashboard.switch.updateDeviceSwitchPort(serial, port, enabled=False)
    print(f"Disabled ports: {ports}")

# Function to enable switch ports
def enable_ports(ports):
    for serial, port in ports:
        dashboard.switch.updateDeviceSwitchPort(serial, port, enabled=True)
    print(f"Enabled ports: {ports}")

# Get all organizations
organizations = dashboard.organizations.getOrganizations()

# Prepare combined CSV file
csv_file = 'clients_with_251_in_third_octet_combined.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Network Name', 'Client Description', 'IP Address', 'Switch Name', 'Switch Port'])

    # Iterate through each organization
    for org in organizations:
        org_id = org['id']
        networks = dashboard.organizations.getOrganizationNetworks(org_id)

        # Iterate through each network in the organization
        for network in networks:
            network_id = network['id']
            network_name = network['name']

            # Initialize variables for pagination
            clients = []
            per_page = 1000  # Number of clients per page
            starting_after = None

            # Retrieve clients with pagination
            while True:
                response = dashboard.networks.getNetworkClients(
                    network_id, timespan=2*60*60, perPage=per_page, startingAfter=starting_after
                )
                clients.extend(response)
                if len(response) < per_page:
                    break
                starting_after = response[-1]['id']

            print(f"Total clients found in network {network_name}: {len(clients)}")

            # Collect ports to disable/enable per network
            ports_to_toggle = []

            # Check each client for matching IP address and get switch port details
            for client in clients:
                print(f"Checking client: {client['description']} with IP: {client.get('ip', 'No IP')}")
                if 'ip' in client and is_matching_ip(client['ip']):
                    switch_name = client.get('recentDeviceName')
                    switch_port = client.get('switchport')
                    switch_serial = client.get('recentDeviceSerial')
                    print(f"Switch details: {switch_name}, Port: {switch_port}")
                    writer.writerow([network_name, client['description'], client['ip'], switch_name, switch_port])
                    print(f"Match found: {client['description']} with IP: {client['ip']} on switch {switch_name} port {switch_port}")

                    # Add to list of ports to toggle per network
                    if switch_serial and switch_port:
                        ports_to_toggle.append((switch_serial, switch_port))

            # Disable all ports in the current network
            disable_ports(ports_to_toggle)
            time.sleep(30)  # Wait for 30 seconds
            # Enable all ports in the current network
            enable_ports(ports_to_toggle)

print("Clients with IP addresses having 251 in the third octet have been listed in a combined CSV file.")
