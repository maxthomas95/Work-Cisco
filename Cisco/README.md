# Cisco Automation Hub

This directory serves as the centralized hub for automating Cisco network infrastructure using **Ansible** and **Terraform**. It provides modular tooling to simplify both configuration management and infrastructure provisioning across on-premises Cisco platforms.

---

## 📁 Submodules


### 🛠 [`Ansible/`](./Ansible)
- Declarative configuration management for Cisco devices
- Supports platforms like **NX-OS** and **IOS-XE**
- Includes modules for:
  - 🔒 [RADIUS](./Ansible/Radius)
  - 🕒 [NTP](./Ansible/NTP)

### ⚙️ [`Terraform/`](./Terraform)
- Infrastructure-as-Code (IaC) automation
- Current focus: [BGP Peering Setup](./Terraform/BGP) on Cisco Nexus switches via hybrid Terraform + Ansible workflow

---

## 🚀 Getting Started

1. Review the `README.md` in each subdirectory for module-specific instructions
2. Clone this repository and navigate to the relevant toolset:
   ```bash
   git clone https://github.com/<your-org>/Work-Cisco.git
   cd Work-Cisco/Cisco/Ansible  # or Terraform
   ```
3. Set up required variables (`.env`, `vault`, or `*.tfvars`)
4. Run Ansible playbooks or Terraform workflows as needed

---

## 🔧 Common Requirements

- Python 3.8+
- Ansible 2.10+ and Terraform 1.0+
- Required Ansible collections:  
  - `ansible.netcommon`  
  - `cisco.nxos`, `cisco.ios`
- Cisco device credentials stored securely (preferably via Ansible Vault or environment injection)

---