# Cisco Terraform Automation

This directory contains Terraform-based infrastructure automation for Cisco environments. These modules are designed to orchestrate configuration workflows and integrate with tools like **Ansible** for full-stack network automation.

---

## 📦 Available Modules

### 🔁 BGP (Border Gateway Protocol)

- Automates BGP peering configuration on Cisco Nexus switches
- Coordinates Terraform and Ansible to push validated configurations
- Includes input validation, secure credential handling, and output reporting

🔗 See: [`Terraform/BGP/README.md`](./BGP/README.md)

---

## 🛠 Requirements

- Terraform 1.0+
- Remote-exec enabled (typically via SSH)
- Git (for cloning config repos during provisioning)
- Optional: Ansible installed on the control node (for hybrid workflows)

---

## 🧱 Usage Overview

Each module in this directory is self-contained. To use one:

```bash
cd BGP
terraform init
terraform apply
```

> Refer to the module's `README.md` for variable configuration and prerequisites.

---
