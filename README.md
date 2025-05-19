# Work-Cisco Repository

## Overview
This repository contains tools and scripts for managing Cisco networks, including:
- Meraki cloud networks (API integrations)
- On-premises Nexus devices (Terraform/Ansible automation)
- BGP configuration management

## Prerequisites
- Python 3.8+ (for Meraki scripts)
- Terraform 1.0+ (for infrastructure automation)
- Ansible 2.9+ (for network device configuration)
- Meraki Dashboard API access
- Azure Key Vault configured with:
  - Meraki API key
  - Azure service principal credentials
- Environment variables configured in `.env` file

## Setup
1. Clone this repository
2. Install Python dependencies:
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
├── Cisco/                # On-premises Cisco automation
│   └── Terraform/        # Infrastructure as Code
│       └── BGP/          # BGP configuration management
│           ├── main.tf   # Terraform configuration
│           ├── variables.tf
│           ├── hosts.ini # Ansible inventory
│           ├── nexus_bgp.yml # Ansible playbook
│           └── README.md # Detailed BGP documentation
├── Meraki/               # Meraki-specific scripts
│   ├── Meraki_GetAllDevices.py
│   ├── Meraki_VPN_Status.py
│   └── README.md         # Detailed Meraki documentation
├── .env.example          # Environment template
└── README.md             # This file
```

## Key Features
- **Meraki Automation**:
  - Device inventory management
  - VPN status monitoring

- **On-premises Automation**:
  - BGP configuration management
  - Infrastructure as Code deployment
  - Network device provisioning

## Contributing
Please follow standard Git workflow:
1. Create a feature branch
2. Make changes
3. Submit a pull request

For network automation changes:
- Include Terraform plan output
- Document Ansible playbook changes
- Update relevant README files
