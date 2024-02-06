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
echo "=== GOBUSTER ==="
echo "==1 COMMON.TXT 1=="
gobuster dir -w /usr/share/wordlists/dirb/common.txt -u "$url" -o gobuster-common

#gobuster dir -w /usr/share/wordlists/dirb/common.txt -u "$url" -x txt,php -b 404
