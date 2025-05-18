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
key_vault_name = os.getenv('AZURE_KEY_VAULT')

# Set up the Key Vault client
kv_uri = f"https://{key_vault_name}.vault.azure.net"

# Authenticate using ClientSecretCredential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)

# Retrieve the secret
secret_name = "Meraki-API"
API_KEY = client.get_secret(secret_name).value

# Initialize the Meraki API session
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# Get a list of all networks
try:
    networks = dashboard.organizations.getOrganizationNetworks(organizationId='')
except Exception as e:
    print(f"Error fetching network data: {e}")
    networks = []  # Initialize an empty list to avoid issues in the loop

# Iterate through each network and apply the configuration if the name starts with 'VPN'
for network in networks:
    if network['name'].startswith('VPN'):
        try:
            response = dashboard.appliance.updateNetworkApplianceTrafficShapingVpnExclusions(
                network['id'],
                custom=[
        #TalkDesk - Prod
        {'protocol': 'tcp', 'destination': '168.86.128.0/18', 'port': '80'},
        {'protocol': 'tcp', 'destination': '168.86.128.0/18', 'port': '443'},
        {'protocol': 'tcp', 'destination': '168.86.128.0/18', 'port': '3478'},
        {'protocol': 'udp', 'destination': '168.86.128.0/18', 'port': 'any'},

        #TalkDesk - Test Tool
        {'protocol': 'tcp', 'destination': '13.231.194.210/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.231.194.210/32', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.231.194.210/32', 'port': '3478'},
        {'protocol': 'udp', 'destination': '13.231.194.210/32', 'port': '3478'},

        {'protocol': 'tcp', 'destination': '54.169.53.114/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '54.169.53.114/32', 'port': '443'},
        {'protocol': 'tcp', 'destination': '54.169.53.114/32', 'port': '3478'},
        {'protocol': 'udp', 'destination': '54.169.53.114/32', 'port': '3478'},

        {'protocol': 'tcp', 'destination': '3.104.77.47/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '3.104.77.47/32', 'port': '443'},
        {'protocol': 'tcp', 'destination': '3.104.77.47/32', 'port': '3478'},
        {'protocol': 'udp', 'destination': '3.104.77.47/32', 'port': '3478'},

        {'protocol': 'tcp', 'destination': '3.126.75.106/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '3.126.75.106/32', 'port': '443'},
        {'protocol': 'tcp', 'destination': '3.126.75.106/32', 'port': '3478'},
        {'protocol': 'udp', 'destination': '3.126.75.106/32', 'port': '3478'},

        {'protocol': 'tcp', 'destination': '34.241.15.175/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '34.241.15.175/32', 'port': '443'},
        {'protocol': 'tcp', 'destination': '34.241.15.175/32', 'port': '3478'},
        {'protocol': 'udp', 'destination': '34.241.15.175/32', 'port': '3478'},

        {'protocol': 'tcp', 'destination': '54.94.187.166/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '54.94.187.166/32', 'port': '443'},
        {'protocol': 'tcp', 'destination': '54.94.187.166/32', 'port': '3478'},
        {'protocol': 'udp', 'destination': '54.94.187.166/32', 'port': '3478'},

        {'protocol': 'tcp', 'destination': '52.72.1.99/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.72.1.99/32', 'port': '443'},
        {'protocol': 'tcp', 'destination': '52.72.1.99/32', 'port': '3478'},
        {'protocol': 'udp', 'destination': '52.72.1.99/32', 'port': '3478'},

        {'protocol': 'tcp', 'destination': '54.218.117.148/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '54.218.117.148/32', 'port': '443'},
        {'protocol': 'tcp', 'destination': '54.218.117.148/32', 'port': '3478'},
        {'protocol': 'udp', 'destination': '54.218.117.148/32', 'port': '3478'},

        #TeamsVoice - Optimize Requred - ID 11
        {'protocol': 'udp', 'destination': '13.107.64.0/18', 'port': '3478'},
        {'protocol': 'udp', 'destination': '13.107.64.0/18', 'port': '3479'},
        {'protocol': 'udp', 'destination': '13.107.64.0/18', 'port': '3480'},
        {'protocol': 'udp', 'destination': '13.107.64.0/18', 'port': '3481'},

        {'protocol': 'udp', 'destination': '52.112.0.0/14', 'port': '3478'},
        {'protocol': 'udp', 'destination': '52.112.0.0/14', 'port': '3479'},
        {'protocol': 'udp', 'destination': '52.112.0.0/14', 'port': '3480'},
        {'protocol': 'udp', 'destination': '52.112.0.0/14', 'port': '3481'},

        {'protocol': 'udp', 'destination': '52.122.0.0/15', 'port': '3478'},
        {'protocol': 'udp', 'destination': '52.122.0.0/15', 'port': '3479'},
        {'protocol': 'udp', 'destination': '52.122.0.0/15', 'port': '3480'},
        {'protocol': 'udp', 'destination': '52.122.0.0/15', 'port': '3481'},

        #TeamsVoice - Allow Required - ID 12
        {'protocol': 'tcp', 'destination': '13.107.64.0/18', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.107.64.0/18', 'port': '443'},

        {'protocol': 'tcp', 'destination': '52.112.0.0/14', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.112.0.0/14', 'port': '443'},

        {'protocol': 'tcp', 'destination': '52.122.0.0/15', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.122.0.0/15', 'port': '443'},

        {'protocol': 'tcp', 'destination': '52.238.119.141/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.238.119.141/32', 'port': '443'},

        {'protocol': 'tcp', 'destination': '52.244.160.207/32', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.244.160.207/32', 'port': '443'},
        ],
            majorApplications=[]
            )
            print(f"Configuration applied to network '{network['name']}': {response}")
        except Exception as e:
            print(f"Error applying configuration to network '{network['name']}': {e}")