import os
import csv
import meraki
import smtplib
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# ========================================
# Load secrets from Azure + .env
# ========================================
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
print(f"Loading .env file from: {env_path}")
load_dotenv(dotenv_path=env_path)

tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
email_user = os.getenv('EMAIL_USER')
email_recipient = os.getenv('EMAIL_RECIPIENT')
key_vault_name = os.getenv('AZURE_KEY_VAULT')
organization_id = os.getenv('ORGANIZATION_ID')
meraki_secret_name = os.getenv('MERAKI_SECRET_NAME')

# ========================================
# Connect to Azure Key Vault & get Meraki API key
# ========================================
kv_uri = f"https://{key_vault_name}.vault.azure.net"
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)
API_KEY = client.get_secret(meraki_secret_name).value  # TODO: Ensure meraki_secret_name is set in .env

# ========================================
# Initialize Meraki API Client
# ========================================
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# ========================================
# Output CSV setup
# ========================================
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'Output')
os.makedirs(output_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
CSV_FILE = os.path.join(output_dir, f'meraki_errors_{timestamp}.csv')

# ========================================
# Clean network list (no ATM/HE networks)
# ========================================
def get_all_networks():
    try:
        networks = dashboard.organizations.getOrganizationNetworks(organization_id)
        return [
            net for net in networks
            if not (net['name'].startswith('ATM') or (net['name'].startswith('#') and not net['name'].startswith('##')))
        ]
    except Exception as e:
        print(f"[ERROR] Failed to fetch networks: {e}")
        return []

# ========================================
# Helper: Write a row for 169.x.x.x clients
# ========================================
def write_169_row(writer, network_name, device_name, client):
    ip = client.get('ip') or client.get('recentDeviceIp')
    writer.writerow([
        '169 Client IP',
        f"{network_name} - {device_name}",
        client.get('description', 'N/A'),
        client['mac'],
        ip
    ])

# ========================================
# Check for clients with 169.x.x.x IPs
# ========================================
def find_169_client_ips(writer, networks):
    try:
        for network in networks:
            network_id = network['id']
            name = network['name']
            clients = dashboard.networks.getNetworkClients(
                network_id, timespan=86400, perPage=1000, total_pages='all'
            )
            print(f"Clients in {name}: {len(clients)}")
            for client in clients:
                ip = client.get('ip') or client.get('recentDeviceIp')
                if ip and ip.startswith('169'):
                    serial = client.get('recentDeviceSerial')
                    if serial:
                        device = dashboard.devices.getDevice(serial)
                        write_169_row(writer, name, device['name'], client)
                        print(f"169 IP: {ip} on {device['name']} in {name}")
                    else:
                        print(f"169 IP: {ip} (no device serial)")
    except Exception as e:
        print(f"[ERROR] 169 IP check failed: {e}")

# ========================================
# Check MS switches for port errors/warnings
# ========================================
def check_port_status(network_id, writer):
    try:
        devices = dashboard.networks.getNetworkDevices(network_id)
        for device in devices:
            if 'MS' not in device['model']:
                continue
            ports = dashboard.switch.getDeviceSwitchPortsStatuses(device['serial'])
            for port in ports:
                if port.get('enabled') and port.get('status') == 'Connected':
                    issues = []
                    issues.extend(port.get('errors', []))
                    issues.extend(port.get('warnings', []))
                    if issues:
                        issue_list = ', '.join(issues)
                        writer.writerow([
                            'Port Issue',
                            f"{device['name']} - Port {port['portId']}",
                            f"Issues: {issue_list}",
                            port.get('name', 'N/A'),
                            issue_list
                        ])
    except Exception as e:
        print(f"[ERROR] Port check failed: {e}")

# ========================================
# Run switch port check across all valid networks
# ========================================
def check_all_networks(writer, networks):
    for network in networks:
        print(f"Checking network: {network['name']}")
        check_port_status(network['id'], writer)

# ========================================
# Email CSV report as attachment
# ========================================
def send_email(csv_file):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_recipient
    msg['Subject'] = f'Meraki Health Check Report - {timestamp}'

    with open(csv_file, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(csv_file)}')
        msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(email_user, email_recipient, msg.as_string())
        print(f"Email sent to {email_recipient}")

# ========================================
# Main function — orchestrates everything
# ========================================
def main():
    networks = get_all_networks()  # Fetch once, reuse
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Network/Device Name', 'Description', 'MAC/Port ID', 'IP/Issues'])
        find_169_client_ips(writer, networks)
        check_all_networks(writer, networks)
    send_email(CSV_FILE)

if __name__ == '__main__':
    main()
