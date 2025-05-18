# Meraki Scripts Documentation

## Scripts Overview
1. `Meraki_GetAllDevices.py` - Exports complete device inventory to CSV
2. `Meraki_VPN_Status.py` - Monitors VPN connection status
3. `Meraki_Track_ImportantDevices.py` - Tracks any device ports across switches
4. `Meraki_SplitTunnel_All_VPN_Networks.py` - Configures split tunneling for all VPN networks
5. `Meraki_SplitTunnel_Simple.py` - Configures split tunneling for a single network

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

## Authentication Flow (All Scripts)
1. Load credentials from `.env`
2. Authenticate to Azure Key Vault  
3. Retrieve Meraki API key
4. Connect to Meraki Dashboard API

## Troubleshooting
### Common Issues
- Invalid Azure credentials
- Missing Key Vault permissions
- Expired Meraki API key
- Incorrect organization ID

### Script-Specific
- GetAllDevices: Verify CSV write permissions
- VPN_Status: Check VPN appliance presence
- TrackDevices: Ensure port naming conventions
- SplitTunnel: Validate network IDs
