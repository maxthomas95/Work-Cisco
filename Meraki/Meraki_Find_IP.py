import os
import csv
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
# IP Search Function
# ========================================
def find_client_ips(api_key, csv_file, target_ip):
    try:
        print(f"Starting IP search for: {target_ip}")
        
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Network Name', 'Client Description', 'Client MAC', 'Client IP', 'Device Name', 'Device Model'])

            # Get organization networks
            networks = dashboard.organizations.getOrganizationNetworks(organization_id)
            print(f"Searching {len(networks)} networks in organization {organization_id}")
            
            for network in networks:
                network_id = network['id']
                network_name = network['name']
                
                try:
                    clients = dashboard.networks.getNetworkClients(
                        network_id, 
                        timespan=604800,  # Last 7 days
                        perPage=1000,
                        total_pages='all'
                    )
                    print(f"Checking {len(clients)} clients in {network_name}")
                    
                    for client in clients:
                        client_ip = client.get('ip') or client.get('recentDeviceIp')
                        if client_ip == target_ip:
                            device_serial = client.get('recentDeviceSerial')
                            if device_serial:
                                device = dashboard.devices.getDevice(device_serial)
                                writer.writerow([
                                    network_name,
                                    client.get('description', 'N/A'),
                                    client['mac'],
                                    client_ip,
                                    device['name'],
                                    device['model']
                                ])
                                print(f"Match found: {client_ip} on {device['name']} in {network_name}")
                            else:
                                print(f"Match found (no device): {client_ip} in {network_name}")
                except Exception as e:
                    print(f"[WARNING] Error processing network {network_name}: {e}")
                    continue
                    
        print(f"Search completed. Results saved to {csv_file}")
    except Exception as e:
        print(f"[ERROR] IP search failed: {e}")
        raise

# ========================================
# Main Execution
# ========================================
if __name__ == '__main__':
    target_ip = '192.168.128.6'  # TODO: Set target IP to search for
    CSV_FILE = 'found_ips.csv'  # TODO: Set output CSV path if needed
    
    try:
        find_client_ips(API_KEY, CSV_FILE, target_ip)
    except Exception as e:
        print(f"[ERROR] Script execution failed: {e}")
