# Meraki Scripts Documentation

## Table of Contents
- [Scripts Overview](#scripts-overview)
- [Requirements](#requirements-all-scripts)
- [Usage](#usage-all-scripts)
- [Script Details](#script-details)
- [Authentication Flow](#authentication-flow-all-scripts)
- [Configuration Notes](#configuration-notes)
- [Troubleshooting](#troubleshooting)

## Scripts Overview
1. `Meraki_GetAllDevices.py` - Exports complete device inventory to CSV
2. `Meraki_VPN_Status.py` - Monitors VPN connection status
3. `Meraki_Track_ImportantDevices.py` - Tracks any device ports across switches
4. `Meraki_SplitTunnel_All_VPN_Networks.py` - Configures split tunneling for all VPN networks
5. `Meraki_SplitTunnel_Simple.py` - Configures split tunneling for a single network
6. `Meraki_AP_AddTag.py` - Adds tags to access points
7. `Meraki_AP_GetAllAPInfo.py` - Retrieves all AP information
8. `Meraki_AP_GetAPTags.py` - Gets tags for specific APs
9. `Meraki_ChangeVLAN3rdOctet_AllNetworks.py` - Updates VLAN third octet across networks
10. `Meraki_ChangeVLAN3rdOctet_Simple.py` - Updates VLAN third octet for single network
11. `Meraki_Check_AllErrors.py` - Checks for common configuration errors
12. `Meraki_Create-TD-Kiosk.py` - Creates TalkDesk kiosk configuration
13. `Meraki_Find_IP.py` - Locates specific IP in network
14. `Meraki_FW_L3_Append_Rules.py` - Appends firewall rules
15. `Meraki_FW_L3_Rules_ALL_VPN-Networks.py` - Configures firewall rules for VPN networks
16. `Meraki_FW_L3_Rules_Simple.py` - Configures basic firewall rules
17. `Meraki_Get_SecondOctet.py` - Retrieves second octet information
18. `Meraki_GetAllNetworks.py` - Lists all networks
19. `Meraki_GetPublicIPs.py` - Gets public IP information
20. `Meraki_Kill_Script_Auto.py` - Automated script termination
21. `Meraki_Kill_Script_Manual.py` - Manual script termination
22. `Meraki_Reboot_AllAPs.py` - Reboots all access points
23. `Meraki_Reboot_TeamsPhones_All.py` - Reboots all Teams phones
24. `Meraki_Reboot_TeamsPhones_Simple.py` - Reboots Teams phones in single network

## 📘 Naming Convention

Scripts in this repo follow two common patterns:

- **`Simple`** – Targets a **single Meraki network** that must be specified manually (via a hardcoded value or `.env` file)
- **`All`** – Operates across **all networks in the organization**, using the Org ID from `.env`

> 🔧 Use `Simple` scripts for testing or small-scope changes. Use `All` scripts when applying changes org-wide.

---

## 📂 Script Categories

### 🧾 Inventory & Reporting
- `Meraki_GetAllDevices.py` – Export device inventory to CSV  
- `Meraki_GetAllNetworks.py` – List all networks in organization  
- `Meraki_GetPublicIPs.py` – Get public IPs for all networks  
- `Meraki_Find_IP.py` – Locate a specific IP address  
- `Meraki_AP_GetAllAPInfo.py` – Retrieve all AP info  
- `Meraki_AP_GetAPTags.py` – Get tags for specific APs  
- `Meraki_Get_SecondOctet.py` – Report second octet info (IP addressing logic)

### 🔒 Configuration – VLAN, Split Tunnel, Firewall
- `Meraki_ChangeVLAN3rdOctet_AllNetworks.py` – Update VLAN octets across org  
- `Meraki_ChangeVLAN3rdOctet_Simple.py` – Update VLAN octet for one network  
- `Meraki_SplitTunnel_All_VPN_Networks.py` – Configure split tunnel for all VPN networks  
- `Meraki_SplitTunnel_Simple.py` – Split tunnel setup for one VPN network  
- `Meraki_FW_L3_Rules_ALL_VPN-Networks.py` – Configure firewall rules org-wide  
- `Meraki_FW_L3_Rules_Simple.py` – Configure firewall rules for one network  
- `Meraki_FW_L3_Append_Rules.py` – Append firewall rules without overwriting  
- `Meraki_Create-TD-Kiosk.py` – Setup kiosk network config (VLAN, firewall, DHCP)

### ⚙️ Automation & Maintenance
- `Meraki_Track_ImportantDevices.py` – Track critical ports (e.g., cameras)  
- `Meraki_AP_AddTag.py` – Add tags to access points  
- `Meraki_Reboot_AllAPs.py` – Reboot all access points  
- `Meraki_Reboot_TeamsPhones_All.py` – Reboot all Teams phones  
- `Meraki_Reboot_TeamsPhones_Simple.py` – Reboot Teams phones in one network  
- `Meraki_Kill_Script_Auto.py` – Auto-terminate long-running scripts  
- `Meraki_Kill_Script_Manual.py` – Manually terminate a running script  

### 🛡️ Monitoring & Validation
- `Meraki_VPN_Status.py` – Monitor VPN tunnel status  
- `Meraki_Check_AllErrors.py` – Check for common misconfigurations  


## Requirements (All Scripts)
- Meraki API key stored in Azure Key Vault
- Azure service principal credentials
- Organization ID in environment variables
- Python 3.8+ with required packages

## Usage (All Scripts)
```bash
python script_name.py
```

## Script Details

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

## Authentication Flow (All Scripts)
1. Load credentials from `.env`
2. Authenticate to Azure Key Vault  
3. Retrieve Meraki API key
4. Connect to Meraki Dashboard API

## Configuration Notes
### Important TODOs
1. Network IDs must be updated in:
   - Meraki_SplitTunnel_Simple.py
   - Meraki_Reboot_TeamsPhones_Simple.py  
   - Meraki_Kill_Script_Manual.py
   - Meraki_Get_SecondOctet.py
   - Meraki_FW_L3_Rules_Simple.py
   - Meraki_FW_L3_Append_Rules.py
   - Meraki_Create-TD-Kiosk.py
   - Meraki_AP_GetAPTags.py
   - Meraki_AP_GetAllAPInfo.py
   - Meraki_AP_AddTag.py

2. VLAN IDs need configuration in:
   - Meraki_Get_SecondOctet.py
   - Meraki_GetAllNetworks.py
   - Meraki_FW_L3_Rules_Simple.py
   - Meraki_FW_L3_Rules_ALL_VPN-Networks.py
   - Meraki_ChangeVLAN3rdOctet_Simple.py
   - Meraki_ChangeVLAN3rdOctet_AllNetworks.py

3. IP/CIDR ranges require updates in:
   - Meraki_FW_L3_Rules_Simple.py
   - Meraki_FW_L3_Rules_ALL_VPN-Networks.py
   - Meraki_FW_L3_Append_Rules.py
   - Meraki_Create-TD-Kiosk.py

## Troubleshooting
### Common Issues
- Invalid Azure credentials
- Missing Key Vault permissions  
- Expired Meraki API key
- Incorrect organization ID
- Unconfigured network/VLAN IDs

### Script-Specific
- GetAllDevices: Verify CSV write permissions
- VPN_Status: Check VPN appliance presence
- TrackDevices: Ensure port naming conventions
- SplitTunnel: Validate network IDs
- Firewall scripts: Confirm CIDR ranges
- AP scripts: Verify tag naming
- Reboot scripts: Check device connectivity
