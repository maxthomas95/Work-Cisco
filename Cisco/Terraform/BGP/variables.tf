variable "test_vnet_prefix" {
  description = "The virtual network prefix in CIDR notation (e.g. '10.0.0.0/16') used for BGP peering configuration"
  type        = string
  validation {
    condition     = can(regex("^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}/\\d{1,2}$", var.test_vnet_prefix))
    error_message = "Must be a valid CIDR notation (e.g. '10.0.0.0/16')"
  }
}
variable "ansible_vm_ip" {
  description = "IP address or FQDN of the Ansible control node that will execute the BGP configuration"
  type        = string
  validation {
    condition     = can(regex("^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$|^[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", var.ansible_vm_ip))
    error_message = "Must be a valid IP address or FQDN"
  }
}
variable "ansible_vm_user" {
  description = "Privileged username with sudo access on the Ansible control node"
  type        = string
  default     = "admin"  # Default admin username
}
variable "ansible_vm_password_base64" {
  description = "Base64 encoded password for the Ansible control node user. Note: Consider using SSH keys instead for production environments"
  type        = string
  sensitive   = true
  validation {
    condition     = can(base64decode(var.ansible_vm_password_base64))
    error_message = "Must be a valid base64 encoded string"
  }
}
