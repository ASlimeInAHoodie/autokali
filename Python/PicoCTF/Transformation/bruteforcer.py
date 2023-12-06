#!/usr/bin/env python
### UTF-16 BRUTEFORCER
## DESCRIPTION:
# This script was developed to beat the PicoCTF challenge "Transformation". Basically, this
# script uses the same encoding algorithm and compares the encoded data to the data stored
# in the file input. If they are the same, then the flag is the value bruteforced. The script
# does this through increments of two ascii characters. Since each UTF-8 (or 16 in this case)
# is technically two ascii characters, we can get away with this method. Comparing the
# encoded two characters to the already encoded file content, we can check if they match. If
# they do not match, we try the next character in the combo. If they do match, we know more
# of the flag and write to the flag, which then loops again until we have the full flag.
# I have included `test.txt` and `enc` as well so that you may test the script and see it in
# action.
## ARGUMENTS:
# Args              | Description                                   | Input     | Defaults
# ----              | ----                                          | ----      | ----      
# -f, --file        | What file to compare to - the flag.txt        | FILENAME  | ./enc
# -w, --word        | Do you know the start of the string?          | STRING    | EMPTY ('')
# -s, --status      | The frequency of updates, every ^2x10 tries.  | INT       | 4
# -v, --verbose     | Do you want extra output?                     | BOOLEAN   | False
# -n, --keepnewline | Do you want to remove newlines from file data?| BOOLEAN   | True

## IMPORTS
# Required
import string
# QoL
import argparse

# Arguement parsing
parser = argparse.ArgumentParser( prog='UTF-16 Flag Bruteforcer', description='Bruteforce a UTF-16 string, built for the PicoCTF challenge "Transformation". Read source code for instructions.', epilog='made by ASlimeInAHoodie in nano (the best python IDE)' )
parser.add_argument('-f', '--file', default='./enc')
parser.add_argument('-w', '--word', default='')
parser.add_argument('-s', '--status', default='4')
parser.add_argument('-v', '--verbose', action='store_true', default=False)
parser.add_argument('-n', '--keepnewline', action='store_false', default=True)

# Custom error handler
class InputError(Exception):
 pass

## LOAD AND VALIDATE ARGUMENTS
# Load args into args variable
args = parser.parse_args()

file_name = args.file
flag = args.word
frequency =  pow(int(args.status)*10, 2)
verbose = args.verbose
verbose = verbose == 'True' or verbose == 'true' or verbose == 'TRUE' or verbose == True
newline = args.keepnewline
newline = newline == 'True' or newline == 'true' or newline == 'TRUE' or newline == True

## GRAB AND VALIDATE FILE DATA
# Collect the binary data from file
with open(file_name, 'rb') as file:
 enc = file.read()
 file.close()
# Check if new line exists and remove it (for testing purposes)
if (newline and enc[-1:] == b'\n'):
 if (verbose): print("Verbose Status: New line detected...")
 enc = enc[:-1]
enc_ascii = enc.decode('utf-8')
if (verbose): print("Verbose Status: Using file " + file_name + " (BYTE SIZE: " + str(len(enc)) + ")")

## ENCRYPTION FUNCTION
# Convert normal, human readable ascii text to UTF-8 encrypted text
def encrypt(ascii):
 ascii_bytes = str.encode(ascii)
 ascii_encoded = ''.join([chr((ascii_bytes[i] << 8) + ascii_bytes[i + 1]) for i in range(0, len(ascii_bytes), 2)]) # Change this based on your encoding method
 return ascii_encoded

## BEGIN LOOP
print("Brute forcing " + file_name + " with flag: " + flag )
count = 0
while True:
 # Check if current flag is the correct flag
 flag_enc = encrypt(flag)
 if (str.encode(flag_enc) == enc):
  print("Success! The flag for " + file_name + " is: " + flag)
  break
 # Else...
 found = False
 for a in string.printable:
  # If already found, move onto next two characters
  if (found):
   break
  for b in string.printable:
   # Create temp flag with added characters
   _flag = flag + a + b
   # Encrypt temp flag
   _flag_enc = encrypt(_flag)
   # Get temp flag encrypt length
   _flag_enc_length = len(_flag_enc)
   # Check if current quantity of flag is valid or not
   if (_flag_enc == enc_ascii[:_flag_enc_length]):
    if (verbose): print("Verbose Status: TEMP FLAG VALID\n")
    found = True
    flag = _flag
    break;
   ## UPDATER
   # Announce the current progress to the user
   count += 1
   if (count % frequency == 0):
    if (verbose): print("Verbose Status: " + str(len(str.encode(flag_enc))) + "/" + str(len(enc)) + " -> Comparing " + _flag_enc + " and " + enc_ascii[:_flag_enc_length] + " -> Trying: " + _flag)
    else: print("Status: " + str(len(str.encode(flag_enc))) + "/" + str(len(enc)) + " -> Current flag: " + flag)