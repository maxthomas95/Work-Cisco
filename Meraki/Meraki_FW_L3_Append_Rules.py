import os
import meraki

from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

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

# Initialize the Meraki Dashboard API
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# Define the network ID
network_id = 'L_6xxxx'

# Define ACL rules
new_acl_rules = [
    {
        'comment': 'Service1',
        'policy': 'allow',
        'protocol': 'udp',
        'srcCidr': '1.1.1.1/32, 2.2.2.2/32',
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
        'destCidr': '1.1.1.1/32, 8.8.8.8/32',
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
        'srcCidr': '10.xxx.xxx.0/24',
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
