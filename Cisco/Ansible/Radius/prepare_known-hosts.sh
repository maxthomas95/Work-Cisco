#!/bin/bash

# Ensure we're in the directory of the script (in case it's run from elsewhere)
cd "$(dirname "$0")"

# Loop over IPs found in ansible_host assignments
grep 'ansible_host=' hosts.ini | while read -r line; do
  ip=$(echo "$line" | sed -n 's/.*ansible_host=\(.*\)/\1/p' | tr -d '\r')
  if [[ -n "$ip" ]]; then
    if ! ssh-keygen -F "$ip" > /dev/null; then
      echo "Adding $ip to known_hosts..."
      ssh-keyscan -H "$ip" >> ~/.ssh/known_hosts 2>/dev/null
    fi
  fi
done
