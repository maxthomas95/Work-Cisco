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

# Get a list of all networks
try:
    networks = dashboard.organizations.getOrganizationNetworks(organizationId='126960')
except Exception as e:
    print(f"Error fetching network data: {e}")
    networks = []  # Initialize an empty list to avoid issues in the loop

# Iterate through each network and apply the configuration if the name starts with 'VPN'
for network in networks:
    if network['name'].startswith('VPN'):
        try:
            vlan_id = 'xxx'
            response = dashboard.appliance.getNetworkApplianceVlan(
                network['id'], vlan_id
            )

            # Extract the second octet from the 'applianceIp' value
            appliance_ip = response['applianceIp']
            second_octet = appliance_ip.split('.')[1]

            # Define multiple source CIDR addresses
            source_cidrs = [
                f'10.{second_octet}.xxx.0/24',
                f'10.{second_octet}.xxx.0/24'
            ]
            printers_dst_cidrs = [
                f'10.{second_octet}.xxx.0/24',
                f'10.{second_octet}.xxx.0/24'
            ]

            response = dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
                network['id'], 
                rules=[
                    {
                        'comment': 'Service1', 
                        'policy': 'allow', 
                        'protocol': 'tcp', 
                        'destPort': 'Any', 
                        'destCidr': f'10.{second_octet}.xxx.0/24', 
                        'srcPort': 'Any', 
                        'srcCidr': f'10.{second_octet}.xxx.0/24', 
                        'syslogEnabled': True
                    },
                    {
                        'comment': 'Service2', 
                        'policy': 'allow', 
                        'protocol': 'tcp', 
                        'destPort': '55752, 55754, 55756, 55757, 55759', 
                        'destCidr': f'10.{second_octet}.xxx.0/24', 
                        'srcPort': 'Any', 
                        'srcCidr': ','.join(source_cidrs), 
                        'syslogEnabled': True
                    },
                    {
                        'comment': 'Service3', 
                        'policy': 'allow', 
                        'protocol': 'tcp', 
                        'destPort': 'Any', 
                        'destCidr': f'10.{second_octet}.xxx.0/24', 
                        'srcPort': 'Any', 
                        'srcCidr': ','.join(source_cidrs),
                        'syslogEnabled': True
                    },
                    {
                        'comment': 'Service4', 
                        'policy': 'allow', 
                        'protocol': 'tcp', 
                        'destPort': 'Any', 
                        'destCidr': ','.join(printers_dst_cidrs), 
                        'srcPort': 'Any', 
                        'srcCidr': ','.join(source_cidrs),
                        'syslogEnabled': True
                    },
                    {
                        'comment': 'Service5', 
                        'policy': 'allow', 
                        'protocol': 'tcp', 
                        'destPort': 'Any', 
                        'destCidr': f'10.{second_octet}.xxx.0/24', 
                        'srcPort': 'Any', 
                        'srcCidr': ','.join(source_cidrs),
                        'syslogEnabled': True
                    },
                    {
                        'comment': 'Block Inter-VLAN', 
                        'policy': 'deny', 
                        'protocol': 'any', 
                        'destPort': 'Any', 
                        'destCidr': f'10.{second_octet}.0.0/16', 
                        'srcPort': 'Any', 
                        'srcCidr': f'10.{second_octet}.0.0/16',
                        'syslogEnabled': True
                    },
                ]
            )

            print(f"Rules applied for network {network['name']}: {response}")
        except Exception as e:
            print(f"Error applying configuration to network '{network['name']}': {e}")
