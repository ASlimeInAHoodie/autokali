#!/usr/bin/env bash
# ERROR HANDLING
## Check if argument is provided
if [-z "$1"]; then
 echo "Usage: $0 <USERNAME@HOSTNAME>"
 exit 1
fi

# VARIABLES
host="$1"

# MAIN
echo "COPYING TO $host..."
echo "=== SSH             ==="
echo "==1 Trying Command... 1=="
cat ~/.ssh/id_rsa.pub | ssh "$host" "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
## Check exit status of command
if [ "$?" -eq 0 ]; then
  echo "✔ SSH key copied successfully to $host."
else
  echo "=X= Failed to copy SSH key to $host."
  # Can try and run other stuff here too,
fi
