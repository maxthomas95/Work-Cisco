import os
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
# Network Processing
# ========================================
try:
    print(f"Getting networks for organization {organization_id}")
    networks = dashboard.organizations.getOrganizationNetworks(organizationId=organization_id)
    print(f"Found {len(networks)} networks total")
    
    vpn_networks = [n for n in networks if n['name'].startswith('VPN')]
    print(f"Found {len(vpn_networks)} VPN networks to process")

    for network in vpn_networks:
        print(f"\nProcessing VPN network: {network['name']}")
        try:
            vlan_id = 'xxx'  # TODO: Set desired VLAN ID
            print(f"Getting VLAN {vlan_id} configuration")
            vlan = dashboard.appliance.getNetworkApplianceVlan(network['id'], vlan_id)
            
            appliance_ip = vlan['applianceIp']
            second_octet = appliance_ip.split('.')[1]
            print(f"Appliance IP: {appliance_ip}")
            print(f"Using second octet: {second_octet}")

            # Define CIDR ranges
            source_cidrs = [
                f'10.{second_octet}.xxx.0/24',  # TODO: Update source CIDRs
                f'10.{second_octet}.xxx.0/24'   # TODO: Update source CIDRs
            ]
            printers_dst_cidrs = [
                f'10.{second_octet}.xxx.0/24',  # TODO: Update printer CIDRs
                f'10.{second_octet}.xxx.0/24'   # TODO: Update printer CIDRs
            ]

            rules = [
                {
                    'comment': 'Service1', 
                    'policy': 'allow', 
                    'protocol': 'tcp', 
                    'destPort': 'Any', 
                    'destCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Update dest CIDR
                    'srcPort': 'Any', 
                    'srcCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Update src CIDR
                    'syslogEnabled': True
                },
                {
                    'comment': 'Service2', 
                    'policy': 'allow', 
                    'protocol': 'tcp', 
                    'destPort': '55752, 55754, 55756, 55757, 55759', 
                    'destCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Update dest CIDR
                    'srcPort': 'Any', 
                    'srcCidr': ','.join(source_cidrs), 
                    'syslogEnabled': True
                },
                {
                    'comment': 'Service3', 
                    'policy': 'allow', 
                    'protocol': 'tcp', 
                    'destPort': 'Any', 
                    'destCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Update dest CIDR
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
                    'destCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Update dest CIDR
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
                }
            ]

            print("Updating firewall rules...")
            response = dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
                network['id'], 
                rules=rules
            )
            print(f"Successfully updated rules for {network['name']}")
            print(f"- Total rules applied: {len(response['rules'])}")

        except Exception as e:
            print(f"Error processing network {network['name']}: {e}")
            continue

    print("\nCompleted processing all VPN networks")

except Exception as e:
    print(f"\nError processing networks: {e}")
    raise
