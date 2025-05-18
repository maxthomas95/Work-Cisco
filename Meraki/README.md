# Meraki Scripts Documentation

## Scripts Overview
1. `Meraki_GetAllDevices.py` - Exports complete device inventory to CSV
2. `Meraki_VPN_Status.py` - Monitors VPN connection status (documentation pending)

## Meraki_GetAllDevices.py
### Description
Exports all devices in a Meraki organization to CSV format, including:
- Device names and models
- Serial numbers and MAC addresses
- Network associations
- Firmware versions
- IP addresses

### Requirements
- Meraki API key stored in Azure Key Vault
- Azure service principal credentials
- Organization ID in environment variables

### Usage
```bash
python Meraki_GetAllDevices.py
```

### Output
Creates `Output/devices.csv` with columns:
```
Name,Model,Serial,MAC,Network ID,Status,Firmware,IP
```

### Authentication Flow
1. Loads credentials from `.env` file
2. Authenticates to Azure Key Vault
3. Retrieves Meraki API key
4. Connects to Meraki Dashboard API

## Meraki_VPN_Status.py
### Description
Retrieves and displays VPN status information for all appliances in a Meraki organization.

### Features
- Retrieves VPN connection status for all appliances
- Shows active VPN tunnels
- Displays connection uptime and traffic statistics

### Requirements
- Same authentication requirements as GetAllDevices.py
- Organization must have VPN appliances configured

### Usage
```bash
python Meraki_VPN_Status.py
```

### Output
Returns raw JSON data containing:
- VPN tunnel status (up/down)
- Remote gateway information
- Traffic statistics
- Uptime metrics

### Authentication Flow
1. Loads credentials from `.env` file
2. Authenticates to Azure Key Vault
3. Retrieves Meraki API key
4. Connects to Meraki Dashboard API

## Troubleshooting
- Verify Azure credentials in `.env`
- Check Key Vault permissions
- Ensure Meraki API key is valid
- Confirm organization ID matches your Meraki org
