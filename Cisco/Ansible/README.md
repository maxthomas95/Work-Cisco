# Cisco Ansible Automation

This directory contains Ansible playbooks for automating common Cisco device configurations, including **NTP** synchronization and **RADIUS** authentication. These playbooks are designed to work across **NX-OS** and **IOS-XE** platforms.

---

## 📦 Modules

### 🕒 NTP (Time Synchronization)

- Validates and enforces approved NTP server configurations
- Supports: **NX-OS** and **IOS-XE**
- Automatically detects device OS and applies appropriate logic
- Variables file: `ntp_servers.yml` *(optional/shared)*  
- Includes SSH known-hosts fingerprinting playbook for secure NTP sources

🔗 See: [`Ansible/NTP/README.md`](./NTP/README.md)

---

### 🔐 RADIUS (AAA Configuration)

- Configures centralized RADIUS-based authentication for Cisco devices
- Supports:
  - **NX-OS** switches
  - **IOS-XE** routers/switches
- Includes playbooks for cleanup, credential injection, and shared secret rotation
- Uses **Ansible Vault** for encrypted secrets

🔗 See: [`Ansible/Radius/README.md`](./Radius/README.md)

---

## 🚀 Usage

To run a specific module:

```bash
ansible-playbook -i hosts.ini playbook.yml --ask-vault-pass
```

> Replace `playbook.yml` with the target file, such as:
>
> - `NTP/Ansible-NTP.yml`
> - `Radius/NX_OS_configure_radius.yml`

---

## 📋 Requirements

- **Ansible** 2.10+
- Python 3.6+
- Required collections:
  - `cisco.nxos`
  - `cisco.ios`
  - `ansible.netcommon`
- Valid `hosts.ini` inventory grouped by device OS
- Cisco login credentials stored securely in **Ansible Vault**

---

## 🛠 Inventory Example

```ini
[nxos]
switch01 ansible_host=10.1.1.1 ansible_network_os=nxos

[ios_xe]
router01 ansible_host=10.2.2.2 ansible_network_os=ios

[all:vars]
ansible_connection=network_cli
ansible_user=admin
ansible_ssh_pass='{{ vault_password }}'
```

---

