# Work-Cisco Repository

## Overview
This repository contains tools and scripts for managing Cisco Meraki networks through API integrations. The current implementation focuses on device inventory management and VPN status monitoring.

## Prerequisites
- Python 3.8+
- Meraki Dashboard API access
- Azure Key Vault configured with:
  - Meraki API key
  - Azure service principal credentials
- Environment variables configured in `.env` file

## Setup
1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure `.env` file with:
```
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
AZURE_KEY_VAULT=your_keyvault_name
ORGANIZATION_ID=your_meraki_org_id
```

## Directory Structure
```
Work-Cisco/
├── Meraki/               # Meraki-specific scripts
│   ├── Meraki_GetAllDevices.py
│   ├── Meraki_VPN_Status.py
│   └── README.md         # Detailed Meraki documentation
├── .env.example          # Environment template
└── README.md             # This file
```

## Contributing
Please follow standard Git workflow:
1. Create a feature branch
2. Make changes
3. Submit a pull request
