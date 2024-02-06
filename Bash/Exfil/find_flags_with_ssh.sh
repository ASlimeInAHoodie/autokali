#!/bin/bash
# ERROR HANDLING
## Check if argument is provided
if [-z "$1"]; then
 echo "Usage: $0 <USERNAME@HOSTNAME> <STRING> [DIR]"
 exit 1
fi

# VARIABLES
host="$1"
flag="$2"
dir="${3:-.}"

# MAIN
echo "FINDING ON $host"
echo "=== SSH             ==="
echo "==1 Trying Command... 1=="
sshpass -f ~/.ssh/sshpass -P passphrase ssh "$host" "find $dir -type f -exec strings {} + | grep -i $flag"
