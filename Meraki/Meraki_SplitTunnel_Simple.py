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

network_id = 'L_1111111111'  # Replace with your actual network ID

response = dashboard.appliance.updateNetworkApplianceTrafficShapingVpnExclusions(
    network_id, 
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

        #Intune - ID 163 
        {'protocol': 'tcp', 'destination': '104.46.162.96/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '104.46.162.96/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.67.13.176/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.67.13.176/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.67.15.128/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.67.15.128/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.69.231.128/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.69.231.128/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.69.67.224/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.69.67.224/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.70.78.128/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.70.78.128/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.70.79.128/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.70.79.128/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.71.199.64/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.71.199.64/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.73.244.48/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.73.244.48/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.74.111.192/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.74.111.192/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.77.53.176/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.77.53.176/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.86.221.176/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.86.221.176/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.89.174.240/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.89.174.240/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '13.89.175.192/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '13.89.175.192/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.189.229.0/25', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.189.229.0/25', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.191.167.0/25', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.191.167.0/25', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.37.153.0/24', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.37.153.0/24', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.37.192.128/25', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.37.192.128/25', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.38.81.0/24', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.38.81.0/24', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.41.1.0/24', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.41.1.0/24', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.42.1.0/24', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.42.1.0/24', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.42.130.0/24', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.42.130.0/24', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.42.224.128/25', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.42.224.128/25', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.43.129.0/24', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.43.129.0/24', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.44.19.224/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.44.19.224/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.49.93.160/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.49.93.160/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.119.8.128/25', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.119.8.128/25', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.67.121.224/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.67.121.224/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.70.151.32/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.70.151.32/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.71.14.96/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.71.14.96/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.74.25.0/24', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.74.25.0/24', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.78.245.240/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.78.245.240/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.78.247.128/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.78.247.128/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.79.197.64/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.79.197.64/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.79.197.96/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.79.197.96/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.80.180.208/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.80.180.208/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.80.180.224/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.80.180.224/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.80.184.128/25', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.80.184.128/25', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.82.248.224/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.82.248.224/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '40.82.249.128/25', 'port': '80'},
        {'protocol': 'tcp', 'destination': '40.82.249.128/25', 'port': '443'},
        {'protocol': 'tcp', 'destination': '52.150.137.0/25', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.150.137.0/25', 'port': '443'},
        {'protocol': 'tcp', 'destination': '52.162.111.96/28', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.162.111.96/28', 'port': '443'},
        {'protocol': 'tcp', 'destination': '52.168.116.128/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.168.116.128/27', 'port': '443'},        
        {'protocol': 'tcp', 'destination': '52.182.141.192/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.182.141.192/27', 'port': '443'},        
        {'protocol': 'tcp', 'destination': '52.236.189.96/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.236.189.96/27', 'port': '443'},
        {'protocol': 'tcp', 'destination': '52.240.244.160/27', 'port': '80'},
        {'protocol': 'tcp', 'destination': '52.240.244.160/27', 'port': '443'},        
        {'protocol': 'tcp', 'destination': '20.204.193.12/30', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.204.193.12/30', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.204.193.10/31', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.204.193.10/31', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.192.174.216/29', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.192.174.216/29', 'port': '443'},
        {'protocol': 'tcp', 'destination': '20.192.159.40/29', 'port': '80'},
        {'protocol': 'tcp', 'destination': '20.192.159.40/29', 'port': '443'},
        ],
        majorApplications=[]
)

print(response)