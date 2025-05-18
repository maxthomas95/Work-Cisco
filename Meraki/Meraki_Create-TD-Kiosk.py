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
network_id = 'L_xxxx'  # TODO: Update with target network ID

# ========================================
# ACL Rules Configuration
# ========================================
new_acl_rules = [
    {
        'comment': 'Service1',
        'policy': 'allow',
        'protocol': 'udp',
        'srcCidr': 'x.x.x.x/32, x.x.x.x/32',  # TODO: Update source CIDRs
        'srcPort': '67,68',
        'destCidr': 'any',
        'destPort': '67,68'
    },
    {
        'comment': 'Service2',
        'policy': 'allow',
        'protocol': 'udp',
        'srcCidr': 'any',
        'srcPort': '67,68',
        'destCidr': '10.xxx.xxx.0/32, 10.xxx.xxx.0/32',
        'destPort': '67,68'
    },
    {
        'comment': 'Service3',
        'policy': 'deny',
        'protocol': 'any',
        'srcCidr': '10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16',
        'srcPort': 'any',
        'destCidr': '10.xxx.xxx.0/24',
        'destPort': 'any'
    },
    {
        'comment': 'Service4',
        'policy': 'deny',
        'protocol': 'any',
        'srcCidr': 'x.x.x.x/24',
        'srcPort': 'any',
        'destCidr': '10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16',
        'destPort': 'any'
    }
]

try:
    # Retrieve current ACL rules
    current_rules = dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
    print("Current ACL rules retrieved successfully.")
    
    # Identify and remove the existing DENY rule
    deny_rule = None
    for rule in current_rules['rules']:
        if rule['policy'] == 'deny':
            deny_rule = rule
            current_rules['rules'].remove(rule)
            print("Existing DENY rule identified and removed.")
            break

    # Append new rules to the current rules
    combined_rules = current_rules['rules'] + new_acl_rules
    print("New ACL rules appended to current rules.")

    # Re-append the DENY rule at the end
    if deny_rule:
        combined_rules.append(deny_rule)
        print("Existing DENY rule re-appended at the end.")

    # Update ACL rules with the combined list
    response = dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
        network_id, rules=combined_rules
    )
    print("ACL rules updated successfully.")
    print(response)
except Exception as e:
    print(f"Error updating ACL rules: {e}")


# ========================================
# VLAN Configuration
# ========================================
vlan = {
    'id': xxx,  # TODO: Set VLAN ID
    'name': 'VLAN_NAME',  # TODO: Set VLAN name
    'subnet': '10.xxx.xxx.0/24',  # TODO: Set subnet
    'applianceIp': '10.xxx.xxx.1',  # TODO: Set appliance IP
    'dhcpHandling': 'Relay DHCP to another server', # TODO: Change if needed
    'dhcpRelayServerIps': ['10.xxx.xxx.1', '10.xxx.xxx.2'],  # TODO: Set DHCP relay IPs
}

try:
    print(f"Creating VLAN {vlan['id']} on network {network_id}")
    response = dashboard.appliance.createNetworkApplianceVlan(
        network_id, **vlan
    )
    print(f"Successfully created VLAN {vlan['id']}")
    print(f"VLAN details: {response}")
except Exception as e:
    print(f"[ERROR] Failed to create VLAN {vlan['id']}: {e}")
    raise
