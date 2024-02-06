#!/bin/bash
# ERROR HANDLING
## Check if address is provided
if [-z "$1"]; then
 echo "Usage: $0 <address> [port]"
 exit 1
fi

# VARIABLES
port="${2:-80}"
url="http://$1:$port"

# MAIN
echo "ENUM $url..."
echo "=== DIRB ==="
echo "==1 BASIC 1=="
dirb "$url" -o dirb-basic
