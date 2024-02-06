#!/usr/bin/env python
### UNZIP2MEM
## DESCRIPTION:
# This script outputs the raw contents of a file within a password protected zip file. Although this means there is no new line
# at the end of the content, it does mean that the exact binary contents is the same as the zipped file (Tested with a 16KB,
# hello world ELF file).
# This has been tested with `zip -e <ZIPNAME> <FILE>` on Ubuntu 22.04.3 LTS, and 7-Zip on Windows 10 - with the ZipCrypto
# Encryption method. AES-256 does not work. Any other zip creation method has not been tested and may not work.
## ARGUMENTS:
# Args      | Description                       | Input     | Defaults
# ----      | ----                              | ----      | ----
# zip       | Where is the zip file?            | FILE      | NONE - REQUIRED
# file      | What file do you want to decrypt? | FILENAME  | NONE - REQUIRED
# password  | What is the password?             | STRING    | NONE - REQUIRED

## IMPORTS
import zipfile
import argparse
import sys

# Arguement parsing
parser = argparse.ArgumentParser( prog='unzip2mem', description='print file data', epilog='made by ASlimeInAHoodie in VS Code' )
parser.add_argument('zip')
parser.add_argument('file')
parser.add_argument('password')

# Load args into args variable
args = parser.parse_args()

zip_file_path = args.zip
zipped_file_name = args.file
password = args.password

with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
    # Set the password for the zip file
    zip_file.setpassword(bytes(password, 'utf-8'))

    # List the contents of the zip file
    file_list = zip_file.namelist()

    # Check if zipped_file_name is in the zip file
    if zipped_file_name in file_list:
        # Extract the contents of zipped_file_name without writing any new files
        with zip_file.open(zipped_file_name, 'r') as flag_file:
            # Print the contents of zipped_file_name
            #print(flag_file.read().decode('utf-8'))
            sys.stdout.buffer.write(flag_file.read())
    else:
        print(f'{zipped_file_name} not found in the {zip_file_path}.')
