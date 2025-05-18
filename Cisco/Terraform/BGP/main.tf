# Step 1: Generate `vnet_prefix.txt` locally
resource "local_file" "vnet_prefix" {
  content  = var.test_vnet_prefix
  filename = "${path.module}/vnet_prefix.txt"
}

# Step 2: Clone the latest git repo (Ensures latest `hosts.ini`)
resource "null_resource" "clone_repo" {
  provisioner "remote-exec" {
    inline = [
      "cd /tmp",
      "rm -rf Infra-Net",
      "GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=no' git clone git@cred+repo"
    ]

    connection {
      type        = "ssh"
      user        = var.ansible_vm_user
      password    = base64decode(var.ansible_vm_password_base64)
      host        = var.ansible_vm_ip
    }
  }
}

# Step 3: Transfer `vnet_prefix.txt` AFTER Cloning Repo
resource "null_resource" "transfer_vnet_prefix" {
  depends_on = [null_resource.clone_repo]

  provisioner "file" {
    source      = "${path.module}/vnet_prefix.txt"
    destination = "/tmp/local-repo/vnet_prefix.txt"

    connection {
      type        = "ssh"
      user        = var.ansible_vm_user
      password    = base64decode(var.ansible_vm_password_base64)
      host        = var.ansible_vm_ip
    }
  }
}

# Step 4: Process `hosts.ini`, Update `known_hosts`, and Run Ansible
resource "null_resource" "run_ansible" {
  depends_on = [null_resource.transfer_vnet_prefix]

  provisioner "remote-exec" {
    inline = [
      # Extract hosts dynamically from `hosts.ini` and add to `known_hosts`
      "cd /tmp/local-repo",
      "awk '/ansible_host=/{print $2}' hosts.ini | cut -d'=' -f2 | while read host; do grep -q \"$host\" ~/.ssh/known_hosts || ssh-keyscan -H $host >> ~/.ssh/known_hosts; done",

      # Debugging: Verify `known_hosts` was updated
      "cat ~/.ssh/known_hosts",

      # Run Ansible Playbook
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
