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
network_id = 'L_6xxxx'  # TODO: Replace with actual network ID

# ========================================
# ACL Rule Configuration
# ========================================
new_acl_rules = [
    {
        'comment': 'Service1',
        'policy': 'allow',
        'protocol': 'udp',
        'srcCidr': '1.1.1.1/32, 2.2.2.2/32',  # TODO: Update source CIDRs
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
        'destCidr': '1.1.1.1/32, 8.8.8.8/32',  # TODO: Update destination CIDRs
        'destPort': '67,68'
    },
    {
        'comment': 'Service3',
        'policy': 'deny',
        'protocol': 'any',
        'srcCidr': '10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16',
        'srcPort': 'any',
        'destCidr': '10.xxx.xxx.0/24',  # TODO: Update destination CIDR
        'destPort': 'any'
    },
    {
        'comment': 'Service4',
        'policy': 'deny',
        'protocol': 'any',
        'srcCidr': '10.xxx.xxx.0/24',  # TODO: Update source CIDR
        'srcPort': 'any',
        'destCidr': '10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16',
        'destPort': 'any'
    }
]

# ========================================
# Update ACL Rules
# ========================================
try:
    print(f"Processing ACL rules for network {network_id}")
    
    # Retrieve current ACL rules
    print("Retrieving current ACL rules...")
    current_rules = dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
    print(f"Found {len(current_rules['rules'])} existing rules")
    
    # Identify and remove the existing DENY rule
    deny_rule = None
    for rule in current_rules['rules']:
        if rule['policy'] == 'deny':
            deny_rule = rule
            current_rules['rules'].remove(rule)
            print(f"Removed existing DENY rule: {rule['comment']}")
            break

    # Append new rules to the current rules
    combined_rules = current_rules['rules'] + new_acl_rules
    print(f"Added {len(new_acl_rules)} new rules")

    # Re-append the DENY rule at the end
    if deny_rule:
        combined_rules.append(deny_rule)
        print("Re-appended DENY rule at the end")

    # Update ACL rules with the combined list
    print("Updating firewall rules...")
    response = dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
        network_id, rules=combined_rules
    )
    
    print("\nSuccessfully updated ACL rules:")
    print(f"- Total rules: {len(response['rules'])}")
    print(f"- Last rule: {response['rules'][-1]['comment']} ({response['rules'][-1]['policy']})")
    
except Exception as e:
    print(f"\nError updating ACL rules: {e}")
    raise
