# Cisco Terraform Provisioning

## Modules
### BGP
- Automated neighbor configuration
- Supports route-maps and prefix-lists
- Validation checks included
- Variables: `bgp_variables.tf`

## Usage
```bash
terraform init
terraform plan
terraform apply
```

## Requirements
- Terraform 1.0+
- Cisco provider configured
- Network team credentials

## Best Practices
- Review plans before apply
- Use workspaces for environments
- Store state securely
