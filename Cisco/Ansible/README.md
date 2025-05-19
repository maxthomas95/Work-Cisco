# Cisco Ansible Automation

## Modules
### NTP
- Manages time synchronization across devices  
- Supports: IOS, NX-OS, IOS-XE
- Validation playbooks included
- Variables file: `ntp_servers.yml`

### Radius
- Centralized AAA configuration
- TACACS+ integration
- Test cases in `tests/` directory

## Usage
```bash
ansible-playbook -i inventory playbooks/main.yml
```

## Requirements
- Ansible 2.10+
- netcommon collection
- Cisco credentials in vault
