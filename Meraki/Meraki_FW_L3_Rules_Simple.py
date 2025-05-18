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
# Network Configuration
# ========================================
network_id = 'L_xxxx'  # TODO: Replace with actual network ID
vlan_id = 'xxx'  # TODO: Replace with actual VLAN ID

print(f"Getting VLAN {vlan_id} configuration for network {network_id}")
try:
    response = dashboard.appliance.getNetworkApplianceVlan(network_id, vlan_id)
    appliance_ip = response['applianceIp']
    second_octet = appliance_ip.split('.')[1]
    print(f"Appliance IP: {appliance_ip}")
    print(f"Using second octet: {second_octet}")

except Exception as e:
    print(f"Error getting VLAN configuration: {e}")
    raise

# ========================================
# Firewall Rule Configuration
# ========================================
source_cidrs = [
    f'10.{second_octet}.xxx.0/24',  # TODO: Replace with actual source CIDRs
    f'10.{second_octet}.xxx.0/24'   # TODO: Replace with actual source CIDRs
]
printers_dst_cidrs = [
    f'10.{second_octet}.xxx.0/24',  # TODO: Replace with actual printer CIDRs
    f'10.{second_octet}.xxx.0/24'   # TODO: Replace with actual printer CIDRs
]

rules = [
    {
        'comment': 'Service1', 
        'policy': 'allow', 
        'protocol': 'tcp', 
        'destPort': 'Any', 
        'destCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Replace with actual dest CIDR
        'srcPort': 'Any', 
        'srcCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Replace with actual src CIDR
        'syslogEnabled': True
    },
    {
        'comment': 'Service2', 
        'policy': 'allow', 
        'protocol': 'tcp', 
        'destPort': '55752, 55754, 55756, 55757, 55759', 
        'destCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Replace with actual dest CIDR
        'srcPort': 'Any', 
        'srcCidr': ','.join(source_cidrs), 
        'syslogEnabled': True
    },
    {
        'comment': 'Service3', 
        'policy': 'allow', 
        'protocol': 'tcp', 
        'destPort': 'Any', 
        'destCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Replace with actual dest CIDR
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
        'destCidr': f'10.{second_octet}.xxx.0/24',  # TODO: Replace with actual dest CIDR
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

# ========================================
# Update Firewall Rules
# ========================================
try:
    print("Updating L3 firewall rules...")
    response = dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
        network_id, 
        rules=rules
    )
    print("Successfully updated firewall rules")
    print("New rules configuration:")
    for rule in response['rules']:
        print(f"- {rule['comment']}: {rule['policy']} {rule['protocol']} from {rule['srcCidr']} to {rule['destCidr']}")

except Exception as e:
    print(f"Error updating firewall rules: {e}")
    raise
