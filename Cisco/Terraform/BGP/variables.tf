variable "test_vnet_prefix" {
  description = "The test VNet prefix for Nexus"
  type        = string
}
variable "ansible_vm_ip" {
  description = "IP address of the Ansible Linux VM"
  type        = string
}

variable "ansible_vm_user" {
  description = "Username for the Ansible Linux VM"
  type        = string
}
variable "ansible_vm_password_base64" {
  description = "Base64 encoded password"
  type        = string
  sensitive   = true
}