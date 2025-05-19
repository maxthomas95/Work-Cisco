# Creates a local file containing the virtual network prefix for BGP configuration
# This file will be used by subsequent steps to configure network devices
resource "local_file" "vnet_prefix" {
  content  = var.test_vnet_prefix  # Input variable containing the network prefix
  filename = "${path.module}/vnet_prefix.txt"  # Output file path
}

# Clone the latest git repo containing network configuration
# Security Note: Disables StrictHostKeyChecking for automation - consider alternatives
resource "null_resource" "clone_repo" {
  provisioner "remote-exec" {
    inline = [
      "cd /tmp",
      "rm -rf Infra-Net",  # Clean up any previous clone
      "GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=no' git clone git@cred+repo"  # Clone with SSH
    ]

    connection {
      type        = "ssh"  # SSH connection type
      user        = var.ansible_vm_user  # Ansible control node username
      password    = base64decode(var.ansible_vm_password_base64)  # Decoded password
      host        = var.ansible_vm_ip  # Ansible control node IP
    }
  }
}

# Copies the network prefix file to the Ansible working directory
resource "null_resource" "transfer_vnet_prefix" {
  depends_on = [null_resource.clone_repo]  # Ensure repo exists first

  provisioner "file" {
    source      = "${path.module}/vnet_prefix.txt"  # Local source file
    destination = "/tmp/local-repo/vnet_prefix.txt"  # Remote destination

    connection {
      type        = "ssh"
      user        = var.ansible_vm_user
      password    = base64decode(var.ansible_vm_password_base64)
      host        = var.ansible_vm_ip
    }
  }
}

# 1. Dynamically updates known_hosts from hosts.ini
# 2. Verifies the update (debugging)
# 3. Executes the BGP configuration playbook
resource "null_resource" "run_ansible" {
  depends_on = [null_resource.transfer_vnet_prefix]  # Wait for file transfer

  provisioner "remote-exec" {
    inline = [
      # Extract hosts from inventory and add to known_hosts if not present
      "cd /tmp/local-repo",
      "awk '/ansible_host=/{print $2}' hosts.ini | cut -d'=' -f2 | while read host; do grep -q \"$host\" ~/.ssh/known_hosts || ssh-keyscan -H $host >> ~/.ssh/known_hosts; done",

      # Debugging: Output known_hosts contents for verification
      "cat ~/.ssh/known_hosts",

      # Execute Ansible playbook to configure BGP on network devices
      # Uses hosts.ini as inventory and nexus_bgp.yml playbook
      "ansible-playbook -i hosts.ini nexus_bgp.yml"
    ]

    connection {
      type        = "ssh"
      user        = var.ansible_vm_user
      password    = base64decode(var.ansible_vm_password_base64)
      host        = var.ansible_vm_ip
    }
  }
}
