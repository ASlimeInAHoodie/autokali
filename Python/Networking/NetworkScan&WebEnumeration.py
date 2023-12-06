#!/usr/bin/python
### NETWORK SCANNER & WEB ENUMERATION SCRIPT
##  made by ASlimeInAHoodie in nano (the best IDE)
##  only enumerates port 80 by default and only works with subnets 255.255.255.0 and above.

# Required imports
import os
import argparse
import subprocess

# Arguement parsing
parser = argparse.ArgumentParser( prog='Network Scan & Web Enumerator', description='Scans a network and enumerates web services', epilog='made by ASlimeInAHoodie in nano (the best python IDE)' )
parser.add_argument('startipaddress')
parser.add_argument('-e', '--endipaddress', default=False)
parser.add_argument('wordlist')
parser.add_argument('-f', '--file', default='./scan.txt')
parser.add_argument('-w', '--pingwaittime', default='2')
parser.add_argument('-s', '--pingstatusfrequency', default='8')
parser.add_argument('-v', '--verbose', default=True)

# Proves that the script is running (A status percentage is sent later - default is every 8 ips scanned)
print("Loading...")

# Custom error handler
class InputError(Exception):
 pass

## LOAD AND VALIDATE ARGUMENTS
# Load args into args variable
args = parser.parse_args()

# Start Ip Address Validation
Address = args.startipaddress.split('.')
if ( len(Address) != 4 ):
 raise InputError("Invalid start ip address (Too many '.')")
if ( '/' in Address[3] ): # Validate subnet mask
 mask = Address[3].split('/')
 if ( len(mask) > 2 ):
  raise InputError("Invalid start ip address (Too many '/')")
 try:
  int(mask[1])
 except Exception:
  raise InputError("Invalid start ip address (Mask in not an integer)")
 Address[3] = mask[0]
 Address.append(int(mask[1]))
 if ( Address[4] > 32 or Address[4] < 0 ):
  raise InputError("Invalid start ip address (Mask is not valid)")
 elif ( Address[4] < 24):
  raise InputError("Script limitation (Mask is not within scope of script)\nNote: Only masks between 24 and 32 work. You may edit this script to allow for larger subnets, however they have not been tested.")
for octet in Address:
 try:
  int(octet)
 except Exception:
  raise InputError("Invalid start ip address (Octets are not integers)")

# End Ip Address Validation
EndAddress = args.endipaddress
if ( EndAddress != False ):
 EndAddress = EndAddress.split('.')
 if ( len(EndAddress) != 4 ):
  raise InputError("Invalid end ip address (Too many '.')")
 for octet in EndAddress:
  try:
   int(octet)
  except Exception:
   raise InputError("Invalid end ip address (Octets are not integers)")
 EndAddress[3] = str(int(EndAddress[3]) + 1)

# Ip Address Comparrison Validation
if ( len(Address) != 5 and EndAddress == False ):
 raise InputError("Invalid ip address range (Either add a mask or include end address)")
elif ( len(Address) == 5 and EndAddress != False ):
 raise InputError("Invalid ip address range (Both mask and end address are included)")
if ( EndAddress != False and Address[3] > EndAddress[3] ):
 raise InputError("Invalid ip address range (Fourth octet in start ip address too big)\nNote: Max subnet of 255.255.255.0 defined within script, you are welcome to edit this script to increase size, but will result in errors.")

# Update end address if mask exists
if ( EndAddress == False ):
 EndAddress = [Address[0], Address[1], Address[2], str(int(Address[3]) + 1 + pow(2, 32-Address[4]))]
 if ( int(EndAddress[3]) > 256):
  EndAddress[3] = str(256)
 Address.pop()

# Wordlist Validation
Wordlist = args.wordlist
if ( os.path.exists(Wordlist) == False):
 raise InputError("Invalid wordlist (Does not exist)")
elif ( os.access(Wordlist, os.R_OK) == False):
 raise InputError("Invalid wordlist (Unable to read file)")

# Ping wait time Validation
try:
 Ping_waitTime = int(args.pingwaittime)
except Exception:
 raise InputError("Invalid ping wait time (Not an integer)")

# Status frequency Validation
try:
 Ping_statusFrequency = int(args.pingstatusfrequency)
except Exception:
 raise InputError("Invalid ping status frequency (Not an integer)")

# File output Validation and creation
File = args.file
if ( File != "False" and os.path.exists(File) and os.access(File, os.W_OK) == False ):
 raise InputError("Invalid output file (Unable to write to file)")
elif ( File != "False" ):
 if ( os.path.exists(File) == False):
  OutFile = open(File, "x")
 else:
  OutFile = open(File, "w")
# Validation completed

## MAIN
verbose = args.verbose
verbose = verbose == 'True' or verbose == 'true' or verbose == 'TRUE' or verbose == True
quantity = int(EndAddress[3]) - int(Address[3])
count = 0
found_ip = 0
found_web = 0
found_page = 0
while ( int(Address[3]) < int(EndAddress[3]) ):
 count += 1
 response = subprocess.run(["ping", "-c", "1", "-W", str(Ping_waitTime), ".".join(Address)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
 if ( response.returncode == 0 ):
  if (verbose == True): print("IP has been found! (" + ".".join(Address) + ")")
  OutFile.write("IP has been found!" + ".".join(Address) + "\n")
  found_ip += 1
 if ( count % Ping_statusFrequency == 0 ):
  print("Current Status: " + str( (count / quantity) * 100 ) + "% ( " + str(count) + " / " + str(quantity)  + " )")
 # Is port 80 open?
 response = subprocess.run(["curl", "-s", "http://" + ".".join(Address) + ":80/", "-w", '"%{http_code}"', "-o", "/dev/null"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
 if ( response.stdout != '"000"' ):
  if (verbose == True): print("Webserver exists for http://" + ".".join(Address) + ":80/ (Response: " + response.stdout + ")")
  OutFile.write("Webserver exists: http://" + ".".join(Address) + ":80/ (Response: " + response.stdout + ")\n")
  found_web += 1
  found_page += 1
  if (verbose == True): print("Beginning Enumeration...")
  with open(Wordlist) as wordlist:
   for word in wordlist:
    word = word[:-1]
    response = subprocess.run(["curl", "-s", "http://" + ".".join(Address) + ":80/" + str(word) + "/", "-w", '"%{http_code}"', "-o", "/dev/null"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if ( response.stdout != '"000"' and response.stdout != '"404"' ):
     if (verbose == True): print("Page found: http://" + ".".join(Address) + ":80/" + word + "/ (Response: " + response.stdout + ")")
     OutFile.write("Webpage exists: http://" + ".".join(Address) + ":80/" + word + " (Response: " + response.stdout + ")\n")
     found_page += 1
 Address[3] = str(int(Address[3]) + 1)

# Once main is done, print results
print("\nNetwork Scan & Web Enumeration finished!\n")
print("Statistics:")
print("IPs Addresses found: " + str(found_ip))
print("Web Services found:  " + str(found_web))
print("Web Pages found:     " + str(found_page))
OutFile.close()