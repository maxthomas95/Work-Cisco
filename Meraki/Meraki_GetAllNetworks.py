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
# Get MX Devices and Network Info
# ========================================
try:
    print(f"Getting all devices for organization {organization_id}")
    devices = dashboard.organizations.getOrganizationDevices(organization_id)
    
    # Filter to MX devices only
    mx_devices = [device for device in devices if device.get('model', '').startswith('MX')]
    print(f"Found {len(mx_devices)} MX devices")

    # Get network names and second octet for each device
    for device in mx_devices:
        try:
            if 'networkId' in device:
                network = dashboard.networks.getNetwork(device['networkId'])
                device['networkName'] = network['name']
            else:
                device['networkName'] = 'N/A'
            
            # Extract second octet from VLAN IP
            if 'networkId' in device:
                vlan_id = '100'  # TODO: Set target VLAN ID if different
                response = dashboard.appliance.getNetworkApplianceVlan(device['networkId'], vlan_id)
                appliance_ip = response['applianceIp']
                ip_parts = appliance_ip.split('.')
                device['secondOctet'] = int(ip_parts[1]) if len(ip_parts) >= 2 else -1
            else:
                device['secondOctet'] = -1
                
        except Exception as e:
            print(f"[WARNING] Error processing device {device.get('serial', 'unknown')}: {e}")
            device['secondOctet'] = -1
            continue
            
except Exception as e:
    print(f"[ERROR] Failed to get device information: {e}")
    raise

# ========================================
# CSV Output Configuration
# ========================================
def write_to_csv(devices):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, 'Output')
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, 'mx_devices.csv')
        
        seen_networks = set()
        unique_devices = []
        
        for device in devices:
            if device['networkName'] not in seen_networks:
                unique_devices.append(device)
                seen_networks.add(device['networkName'])
        
        unique_devices.sort(key=lambda x: x['secondOctet'])
        
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Network Name', 'Network ID', 'Second Octet'])
            for device in unique_devices:
                writer.writerow([
                    device['networkName'],
                    device.get('networkId', ''),
                    device['secondOctet']
                ])
        
        print(f"\nSuccessfully wrote {len(unique_devices)} unique networks to {csv_path}")
        
    except Exception as e:
        print(f"[ERROR] Failed to write CSV: {e}")
        raise

# ========================================
# Main Execution
# ========================================
if __name__ == '__main__':
    write_to_csv(mx_devices)
