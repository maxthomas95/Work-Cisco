# 📦 Meraki Automation Scripts

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Meraki API](https://img.shields.io/badge/Uses-Meraki%20Dashboard%20API-yellow?logo=cisco&logoColor=white)
![Azure Key Vault](https://img.shields.io/badge/Auth-Azure%20Key%20Vault-blueviolet?logo=microsoftazure&logoColor=white)
![Automation](https://img.shields.io/badge/Automation-Networking-orange?logo=githubactions&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A collection of Python scripts for automating and managing Cisco Meraki networks via the Meraki Dashboard API. Tasks include inventory reporting, firewall/VLAN configuration, AP tagging, and more — all with centralized authentication and reusable code patterns.

---

## 📑 Table of Contents
- [📘 Naming Convention](#-naming-convention)
- [📂 Script Categories](#-script-categories)
- [🛠 Requirements](#-requirements-all-scripts)
- [🚀 Quickstart](#-quickstart)
- [⚙️ Usage](#-usage-all-scripts)
- [📜 Script Details](#-script-details)
- [🔐 Authentication Flow](#-authentication-flow-all-scripts)
- [🧩 Configuration Notes](#-configuration-notes)
- [❗ Troubleshooting](#-troubleshooting)

---

## 📘 Naming Convention

Scripts follow two main patterns:

- **`Simple`** – Targets a **single Meraki network**, manually defined via script variable or `.env`
- **`All`** – Operates across **all networks in the organization** using the Org ID from `.env`

> 🔧 Use `Simple` scripts for small-scope testing. Use `All` scripts for organization-wide automation.

---

## 📂 Script Categories

### 🧾 Inventory & Reporting
- `Meraki_GetAllDevices.py` – Export device inventory to CSV  
- `Meraki_GetAllNetworks.py` – List all org networks  
- `Meraki_GetPublicIPs.py` – Fetch public IP assignments  
- `Meraki_Find_IP.py` – Locate specific IP addresses  
- `Meraki_AP_GetAllAPInfo.py` – Pull detailed AP information  
- `Meraki_AP_GetAPTags.py` – Get tags per AP  
- `Meraki_Get_SecondOctet.py` – Report IP addressing patterns

### 🔒 Configuration – VLANs, Tunnels, Firewalls
- `Meraki_ChangeVLAN3rdOctet_AllNetworks.py` – Bulk VLAN octet updates  
- `Meraki_ChangeVLAN3rdOctet_Simple.py` – VLAN update for single network  
- `Meraki_SplitTunnel_All_VPN_Networks.py` – Set split tunnel rules org-wide  
- `Meraki_SplitTunnel_Simple.py` – Split tunnel config for one network  
- `Meraki_FW_L3_Rules_ALL_VPN-Networks.py` – Org-wide firewall rules  
- `Meraki_FW_L3_Rules_Simple.py` – Single network firewall config  
- `Meraki_FW_L3_Append_Rules.py` – Append rules without overwriting  
- `Meraki_Create-TD-Kiosk.py` – Setup TalkDesk kiosk VLAN/DHCP/firewall

### ⚙️ Automation & Maintenance
- `Meraki_Track_ImportantDevices.py` – Track "Camera" ports across switches  
- `Meraki_AP_AddTag.py` – Tag access points by SSID or name  
- `Meraki_Reboot_AllAPs.py` – Reboot all APs in org  
- `Meraki_Reboot_TeamsPhones_All.py` – Reboot all Teams phones  
- `Meraki_Reboot_TeamsPhones_Simple.py` – Reboot Teams phones per site  
- `Meraki_Kill_Script_Auto.py` – Auto-terminate scripts  
- `Meraki_Kill_Script_Manual.py` – Manual termination

### 🛡️ Monitoring & Validation
- `Meraki_VPN_Status.py` – VPN tunnel monitoring  
- `Meraki_Check_AllErrors.py` – Detect config issues

---

## 🛠 Requirements (All Scripts)

- Python 3.8+
- Required packages (install via `requirements.txt`)
- Meraki API key stored in **Azure Key Vault**
- Azure service principal credentials
- Organization ID stored in environment variables

---

## ⚡ Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/your-org/meraki-scripts.git
cd meraki-scripts

# 2. Set up a .env file
cp .env.example .env  # or create manually

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run your first script
python Meraki_GetAllDevices.py
```

---

## 📝 Example `.env` File

```env
AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_SECRET=your-client-secret
MERAKI_ORG_ID=123456
```

---

## ⚙️ Usage (All Scripts)

```bash
python script_name.py
```

> Output is typically printed to the console and/or written to `Output/` in CSV or JSON format depending on the script.

---

## 📜 Script Details

### Meraki_GetAllDevices.py
#### Description
Exports complete device inventory from Meraki organization to CSV.

#### Features
- Device names, models, serials, MACs
- Network associations and firmware versions
- IP addresses and status

#### Output
CSV file (`Output/devices.csv`) with columns:
```
Name,Model,Serial,MAC,Network ID,Status,Firmware,IP
```

### Meraki_VPN_Status.py  
#### Description
Monitors VPN connection status across organization.

#### Features
- Shows active VPN tunnels
- Displays uptime and traffic stats
- Identifies connection issues

#### Output
Raw JSON with:
- Tunnel status (up/down)
- Gateway info and metrics
- Traffic statistics

### Meraki_Track_ImportantDevices.py
#### Description
Tracks and reports on camera ports across all switches.

#### Features
- Scans all MS switches
- Identifies ports named "Camera"
- Reports network and device info

#### Output
CSV file (`Output/camera_ports.csv`) with:
- Network and device names
- Port IDs and names

### Meraki_SplitTunnel_All_VPN_Networks.py
#### Description
Configures split tunneling rules for all VPN networks.

#### Features
- Applies standardized rules
- Handles TalkDesk and TeamsVoice
- Processes all VPN networks

#### Output
Console confirmation of applied rules

### Meraki_SplitTunnel_Simple.py
#### Description
Configures split tunneling for a single network.

#### Features
- Same rules as All_VPN_Networks
- Targets specific network ID
- Good for testing changes

#### Output
Console confirmation of applied rules

### Meraki_AP_AddTag.py
#### Description
Adds tags to Meraki access points.

#### Features
- Applies tags to specified APs
- Can filter by SSID prefix
- Works with multiple APs

#### Output
Console confirmation of tag additions

### Meraki_AP_GetAllAPInfo.py
#### Description
Retrieves comprehensive AP information.

#### Features
- Gets SSID configurations
- Collects performance metrics
- Reports AP locations

#### Output
JSON data with AP details

### Meraki_AP_GetAPTags.py
#### Description
Gets tags for specific access points.

#### Features
- Lists all tags per AP
- Filters by network
- Shows tag assignments

#### Output
Formatted list of AP tags

### Meraki_ChangeVLAN3rdOctet_AllNetworks.py
#### Description
Updates VLAN third octet across all networks.

#### Features
- Bulk updates VLAN configurations
- Maintains other octets
- Validates changes

#### Output
Console log of changes

### Meraki_ChangeVLAN3rdOctet_Simple.py
#### Description
Updates VLAN third octet for single network.

#### Features
- Targeted VLAN modification
- Simple configuration
- Validation checks

#### Output
Console confirmation

### Meraki_Check_AllErrors.py
#### Description
Checks for common configuration errors.

#### Features
- Scans network settings
- Identifies misconfigurations
- Highlights issues

#### Output
Error report

### Meraki_Create-TD-Kiosk.py
#### Description
Creates TalkDesk kiosk configuration.

#### Features
- Sets up VLANs
- Configures firewall rules
- Establishes DHCP

#### Output
Configuration summary

### Meraki_Find_IP.py
#### Description
Locates specific IP in network.

#### Features
- Searches across devices
- Reports device details
- Outputs to CSV

#### Output
CSV with IP locations

### Meraki_FW_L3_Append_Rules.py
#### Description
Appends firewall rules.

#### Features
- Adds rules without overwriting
- Supports multiple protocols
- Logging options

#### Output
Rule confirmation

### Meraki_FW_L3_Rules_ALL_VPN-Networks.py
#### Description
Configures firewall rules for VPN networks.

#### Features
- Bulk rule application
- Standardized configurations
- Validation

#### Output
Rule application log

### Meraki_FW_L3_Rules_Simple.py
#### Description
Configures basic firewall rules.

#### Features
- Simple rule management
- Single network focus
- Testing friendly

#### Output
Rule confirmation

### Meraki_Get_SecondOctet.py
#### Description
Retrieves second octet information.

#### Features
- Extracts network patterns
- Reports on IP schemes
- Output formatting

#### Output
Second octet details

### Meraki_GetAllNetworks.py
#### Description
Lists all networks.

#### Features
- Complete inventory
- Organization-wide
- Detailed attributes

#### Output
Network list

### Meraki_GetPublicIPs.py
#### Description
Gets public IP information.

#### Features
- Identifies public IPs
- Reports assignments
- Output formatting

#### Output
Public IP report

### Meraki_Kill_Script_Auto.py
#### Description
Automated script termination.

#### Features
- Scheduled termination
- Resource cleanup
- Logging

#### Output
Termination confirmation

### Meraki_Kill_Script_Manual.py
#### Description
Manual script termination.

#### Features
- Controlled shutdown
- Resource cleanup
- Confirmation

#### Output
Termination status

### Meraki_Reboot_AllAPs.py
#### Description
Reboots all access points.

#### Features
- Organization-wide
- Scheduling options
- Status tracking

#### Output
Reboot report

### Meraki_Reboot_TeamsPhones_All.py
#### Description
Reboots all Teams phones.

#### Features
- Bulk operation
- Status monitoring
- Logging

#### Output
Reboot summary

### Meraki_Reboot_TeamsPhones_Simple.py
#### Description
Reboots Teams phones in single network.

#### Features
- Targeted operation
- Quick execution
- Verification

#### Output
Reboot confirmation

---

## 🔐 Authentication Flow (All Scripts)

1. Load credentials from `.env`
2. Authenticate to Azure Key Vault
3. Retrieve Meraki API key
4. Connect to Meraki Dashboard API

---


## 🧩 Configuration Notes

### 🔧 Required Script Modifications

#### 1. Network IDs must be updated in:
- `Meraki_SplitTunnel_Simple.py`
- `Meraki_Reboot_TeamsPhones_Simple.py`  
- `Meraki_Kill_Script_Manual.py`
- `Meraki_Get_SecondOctet.py`
- `Meraki_FW_L3_Rules_Simple.py`
- `Meraki_FW_L3_Append_Rules.py`
- `Meraki_Create-TD-Kiosk.py`
- `Meraki_AP_GetAPTags.py`
- `Meraki_AP_GetAllAPInfo.py`
- `Meraki_AP_AddTag.py`

#### 2. VLAN IDs need configuration in:
- `Meraki_Get_SecondOctet.py`
- `Meraki_GetAllNetworks.py`
- `Meraki_FW_L3_Rules_Simple.py`
- `Meraki_FW_L3_Rules_ALL_VPN-Networks.py`
- `Meraki_ChangeVLAN3rdOctet_Simple.py`
- `Meraki_ChangeVLAN3rdOctet_AllNetworks.py`

#### 3. IP/CIDR ranges require updates in:
- `Meraki_FW_L3_Rules_Simple.py`
- `Meraki_FW_L3_Rules_ALL_VPN-Networks.py`
- `Meraki_FW_L3_Append_Rules.py`
- `Meraki_Create-TD-Kiosk.py`

---

## ❗ Troubleshooting

### 🔄 Common Issues
- ❌ Invalid or missing Azure credentials
- 🔒 Key Vault access denied
- ⏳ Expired Meraki API key
- 🆔 Incorrect or unset Org ID
- ⚙️ Network or VLAN IDs not configured in script

### 🔍 Script-Specific Tips
- `GetAllDevices`: Ensure write access to `Output/`
- `VPN_Status`: Verify MX appliances exist
- `TrackDevices`: Use consistent port names (e.g., "Camera")
- `SplitTunnel`: Double-check target network IDs
- `Firewall Rules`: Validate CIDR/IP format
- `AP Scripts`: Confirm tag names and network IDs
- `Reboot Scripts`: Confirm devices are online and reachable
