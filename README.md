# 🧰 Work-Cisco Repository

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-1.0%2B-623CE4?logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-2.9%2B-black?logo=ansible&logoColor=white)
![Meraki API](https://img.shields.io/badge/API-Meraki%20Dashboard-yellow?logo=cisco&logoColor=white)
![Azure Key Vault](https://img.shields.io/badge/Auth-Azure%20Key%20Vault-blueviolet?logo=microsoftazure&logoColor=white)
![IaC](https://img.shields.io/badge/IaC-Terraform%20%2B%20Ansible-green?logo=devdotto)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

This repository contains automation tools and scripts for managing Cisco networks across both **on-premises** and **cloud-based** environments.

---

### ⚠️ WARNING: USE RESPONSIBLY

> These scripts and tools are powerful.  
> **Do not run in production without testing.**  
> Always validate in a lab or limited environment first.  
> Make sure you **understand what each script does** before executing.  
> **Use at your own risk.**

---

## 🗺️ Overview

Work-Cisco supports both **traditional Cisco infrastructure** (like Nexus switches) and **cloud-managed Meraki networks**. It includes:

- 🌐 **Meraki**: Python scripts leveraging the Meraki Dashboard API  
- 🧱 **Cisco (On-Prem)**: Terraform + Ansible for infrastructure automation and configuration  
- 🔁 **BGP Peering**: Fully automated peering setup for Nexus switches using Terraform-driven Ansible

---

## ⚙️ Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.8+ | Required for Meraki scripts |
| Terraform | 1.0+ | Infrastructure orchestration |
| Ansible | 2.9+ | Network configuration management |
| Azure Key Vault | N/A | Stores Meraki API key and Azure credentials |

✅ Ensure your environment includes:
- A `.env` file (see `.env.example`)
- Access to the Meraki Dashboard API
- An Azure service principal with Key Vault access

---

## 🚀 Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-org/Work-Cisco.git
cd Work-Cisco

# 2. Install Python dependencies (for Meraki)
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Then edit your credentials:
```

```env
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
AZURE_KEY_VAULT=your_keyvault_name
ORGANIZATION_ID=your_meraki_org_id
```

---

## 📁 Directory Structure

```
Work-Cisco/
├── Cisco/                          # On-premises Cisco automation
│   ├── Ansible/                    # Configuration management via playbooks
│   │   ├── NTP/                    # NTP config validation
│   │   ├── Radius/                 # AAA configuration
│   │   └── README.md               # Overview of all playbooks
│   ├── Terraform/                  # Infrastructure as Code (IaC)
│   │   ├── BGP/                    # BGP peering config for Nexus
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── hosts.ini
│   │   │   ├── nexus_bgp.yml
│   │   │   └── README.md
│   │   └── README.md
│   └── README.md                   # Cisco automation hub
├── Meraki/                         # Meraki Dashboard API scripts
│   ├── Meraki_GetAllDevices.py
│   ├── Meraki_VPN_Status.py
│   ├── ...
│   └── README.md                   # Full Meraki script catalog
├── .env.example                    # Environment variable template
└── README.md                       # This file
```

---

## 🔑 Key Features

### ☁️ Meraki Automation
- Device inventory management
- VPN tunnel monitoring
- Firewall, VLAN, and AP configuration
- Centralized authentication via Azure Key Vault

🔗 See: [`Meraki/README.md`](./Meraki/README.md)

---

### 🧱 On-Premises Cisco Automation
- Nexus BGP peering automation
- Hybrid Terraform + Ansible deployment flows
- Modular NTP and RADIUS configuration playbooks

🔗 See: [`Cisco/README.md`](./Cisco/README.md)

---

## 📬 Support / Questions

This repo is actively maintained. For questions, issues, or feature requests, please open a GitHub Issue or contact the maintainers via your preferred internal channel.

---