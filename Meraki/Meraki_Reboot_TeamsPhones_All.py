import os
import csv
import time
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
# Helper Functions
# ========================================
def is_matching_ip(ip):
    """Check if IP has 251 in third octet."""
    if not ip:
        return False
    parts = ip.split('.')
    return len(parts) == 4 and parts[2] == '251'

def toggle_ports(ports, enable):
    """Toggle switch ports (enable/disable)."""
    action = "Enabling" if enable else "Disabling"
    print(f"\n{action} {len(ports)} ports...")
    
    for serial, port in ports:
        try:
            dashboard.switch.updateDeviceSwitchPort(
                serial, port, 
                enabled=enable
            )
            print(f"{action[:-3]}ed port {port} on switch {serial}")
        except Exception as e:
            print(f"[WARNING] Failed to toggle port {port} on {serial}: {e}")

# ========================================
# Main Execution
# ========================================
if __name__ == '__main__':
    try:
        # Set up CSV output
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, 'Output')
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, 'teams_phones_reboot_log.csv')

        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Network Name', 'Client Description', 'IP Address', 'Switch Name', 'Switch Port'])

            print("Getting organizations...")
            organizations = dashboard.organizations.getOrganizations()

            for org in organizations:
                org_id = org['id']
                print(f"\nProcessing organization: {org['name']}")

                networks = dashboard.organizations.getOrganizationNetworks(org_id)
                for network in networks:
                    network_id = network['id']
                    network_name = network['name']
                    print(f"\nChecking network: {network_name}")

                    # Get clients with pagination
                    clients = []
                    per_page = 1000
                    starting_after = None
                    
                    while True:
                        response = dashboard.networks.getNetworkClients(
                            network_id, 
                            timespan=2*60*60, 
                            perPage=per_page, 
                            startingAfter=starting_after
                        )
                        clients.extend(response)
                        if len(response) < per_page:
                            break
                        starting_after = response[-1]['id']

                    print(f"Found {len(clients)} clients")
                    ports_to_toggle = []

                    for client in clients:
                        if 'ip' in client and is_matching_ip(client['ip']):
                            switch_serial = client.get('recentDeviceSerial')
                            switch_port = client.get('switchport')
                            
                            if switch_serial and switch_port:
                                ports_to_toggle.append((switch_serial, switch_port))
                                writer.writerow([
                                    network_name,
                                    client.get('description', ''),
                                    client['ip'],
                                    client.get('recentDeviceName', ''),
                                    switch_port
                                ])

                    if ports_to_toggle:
                        print(f"\nFound {len(ports_to_toggle)} Teams phones to reboot")
                        confirm = input("Confirm port toggle to reboot phones? (y/n): ")
                        if confirm.lower() == 'y':
                            toggle_ports(ports_to_toggle, False)
                            time.sleep(30)
                            toggle_ports(ports_to_toggle, True)
                            print("\nTeams phones reboot completed")
                        else:
                            print("Operation cancelled")
                    else:
                        print("No Teams phones found in this network")

        print(f"\nReport saved to: {csv_path}")

    except Exception as e:
        print(f"[ERROR] Script failed: {e}")
        raise
