#!/bin/bash
# ERROR HANDLING
## Check if argument is provided
if [ -z "$1" ]; then
 echo "Usage: $0 <IP ADDRESS>"
 exit 1
fi

# VARIABLES
target="$1"
dir="nmap"

if [ ! -d "$dir" ]; then
 echo "$dir does not exist. Creating..."
 mkdir "$dir"
fi

# MAIN
echo "NMAPPING $target..."
echo "=== NMAP             ==="
echo "==1 NMAP QUICK 1=="
nmap "$target" -oN nmap/quick -v
echo "==2 NMAP TECHNICAL 2=="
nmap "$target" -sV -sC -oN nmap/tech -v
echo "==3 NMAP ALL TCP 3=="
nmap "$target" -p- -oN nmap/all -v
echo "==4 NMAP ALL UDP 4=="
nmap "$target" -p- -sU -oN nmap/all-udp -v
