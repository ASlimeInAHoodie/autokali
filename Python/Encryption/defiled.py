#!/usr/bin/env python
### DEFILED
## DESCRIPTION:
# This script uses the public and private SSH keys to encrypt and decrypt respectively. When doing
# either, the script copies the file to a <FILE>.backup file, which can then be used to restore the file
# if it becomes corrupted. Note: If you do not want to create the .backup file, you can supply `-c`
# knowing full well of the risks. Always have at least one backup. 
# If both `-e` and `-d` are supplied, the script will conduct a MD5 hash sum test to validate that the
# supplied keys can be used to encrypt and decrypt files successfully. This validation method can only
# be done when you have both the public and private keys.
# You may also use this script to generate SSH keys. Although ill-advised to be used for real SSH
# implementations, these keys can be used to encrypt files safely using this script, or decrypt files
# that were encrypted by this script. Use `-g` and a file path to use this generator.
## ARGUMENTS:
# Args              | Description                                   | Input     | Defaults
# ----              | ----                                          | ----      | ----
# -g, --generator   | Generate public.key and private.key           | FILEPATH  | DO NOT CREATE (False)
# -f, --file        | What file do you want to encrypt/decrypt?     | FILE      | EMPTY ('')
# -e, --encrypt     | What public key should be used to encrypt?    | FILE      | DO NOT ENCRYPT (False)
# -d, --decrypt     | What private key should be used to decrypt?   | FILE      | DO NOT DECRYPT (False)
# -c, --corrupt     | Do you want to risk not creating a backup?    | NONE      | False 

## IMPORTS
import argparse
import os
import shutil
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Arguement parsing
parser = argparse.ArgumentParser( prog='Defiled', description='Encrypt/decrypt a file with SSH keys.', epilog='made by ASlimeInAHoodie in VS Code' )
parser.add_argument('-f', '--file', default='')
parser.add_argument('-g', '--generate', default=False)
parser.add_argument('-e', '--encrypt', default=False)
parser.add_argument('-d', '--decrypt', default=False)
parser.add_argument('-c', '--corrupt', action='store_true', default=False)

# Load args into args variable
args = parser.parse_args()

## FUNCTIONS
# Create the public.key and private.key
def generate_hashfiles(path):
    # File validation
    if path[-1] != "/": path+="/"
    print('Generating keys to path: ' + path)
    if (os.path.exists(path+'private.key') == True or os.path.exists(path+'public.key') == True):
        while True:
            print("Files already exist.")
            ui = input("Overwrite files? Y/N ")
            if ui.upper() == "N":
                print("Goodbye!")
                raise SystemExit(0)
            elif ui.upper() == "Y":
                break
    if (os.path.exists(path+'private.key') and os.access(path+'private.key', os.W_OK) == False) or (os.path.exists(path+'-public.key') and os.access(path+'-public.key', os.W_OK) == False):
        print("Ξ<!>Ξ Error - Unable to write to files")
        raise SystemExit(1)
    
    # Generate keys
    print("Generating RSA keys...")
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )

    # Write files
    print("Writing " + path + "private.key")
    with open(path+'private.key', 'wb') as pfile:
        pfile.write(private_key)
        pfile.close()
    print("Writing " + path + "public.key")
    with open(path+'public.key', 'wb') as pfile:
        pfile.write(public_key)
        pfile.close()
    
    print("Keys generated.")
    # Return keys if needed
    return private_key, public_key

# Backs up a file by copying the file to <FILENAME>.backup
def backup(file):
    if args.corrupt == False:
        print('Creating backup to: ' + file + '.backup')
        try:
            shutil.copyfile(file, file+".backup")
        except:
            print("Ξ<!>Ξ Error - Could not create backup.")
            raise SystemExit(1)

def encrypt(public_key, file):
    # Read files
    print('Using public key: ' + public_key)
    with open(public_key, 'rb') as pkf:
        key_contents = pkf.read()
        pkf.close()
    print('Reading file: ' + file)
    with open(file, 'rb') as f:
        contents = f.read()
        f.close()
    # Cryptography functions
    print('Serializing key...')
    key = serialization.load_ssh_public_key(
        key_contents,
        backend=default_backend()
    )
    print('Encrypting file bytes...')
    return key.encrypt(
        contents,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def encrypt_file(public_key, file):
    # Encrypt content
    _text = encrypt(public_key, file)
    # Write files
    backup(file)
    print('Overwriting file...')
    with open(file, 'wb') as f:
        f.write(_text)
        f.close()
    print('File encrypted!')
    # Return encrypted content if needed
    return _text

def decrypt(private_key, file):
    # Read files
    print('Reading file: ' + file)
    with open(file, 'rb') as f:
        contents = f.read()
        f.close()
    return decrypt_bytes(private_key, contents)

def decrypt_bytes(private_key, file_bytes):
    # Read files
    print('Using private key: ' + private_key)
    with open(private_key, 'rb') as pkf:
        key_contents = pkf.read()
        pkf.close()
    # Cryptography functions
    print('Serializing key...')
    key = serialization.load_ssh_private_key(
        key_contents,
        backend=default_backend(),
        password=None
    )
    print('Decrypting file bytes...')
    return key.decrypt(
        file_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_file(private_key, file):
    # Decrypt file
    _text = decrypt(private_key, file)
    # Write files
    backup(file)
    print('Overwriting file...')
    with open(file, 'wb') as f:
        f.write(_text)
        f.close()
    print('File decrypted!')
    # Return decrypted content if needed
    return _text

def md5sum(content):
    digest = hashes.Hash(
        hashes.MD5(),
        backend=default_backend()
    )
    digest.update(content)
    md5 = digest.finalize()
    return md5.hex()

def verify(public_key, private_key, file):
    # Getting file contents
    print('Reading file: ' + file)
    with open(file, 'rb') as f:
        contents = f.read()
        f.close()
    # Encryption & Decryption
    print("Running encryption function on temp...")
    try:
        temp = encrypt(public_key, file)
    except:
        print("Ξ<!>Ξ Error - Keys do not match")
        raise SystemExit(1)
    print("Running decryption function on temp...")
    try:
        temp = decrypt_bytes(private_key, temp)
    except:
        print("Ξ<!>Ξ Error - Keys do not match")
        raise SystemExit(1)
    # MD5 Sum verification
    print('Verifying signatures...')
    baseMD5 = md5sum(contents)
    tempMD5 = md5sum(temp)
    print('Base file signature: ' + baseMD5)
    print('Temp file signature: ' + tempMD5)
    if (baseMD5 == tempMD5):
        print("Ξ MD5 SUMS MATCH Ξ")
        return True
    print("Ξ<!>Ξ Error - MD5 sums do not match")
    return False

# File validation
def validate_file(file, permission):
    if (os.path.exists(file) == False):
        print("Ξ<!>Ξ Error - File " + file + " does not exist")
        raise SystemExit(1)
    if (os.access(file, permission) == False):
        print("Ξ<!>Ξ Error - Insufficient permissions")
        raise SystemExit(1)


## MAIN
# Title
print("\nΞΞΞΞΞΞΞΞΞΞΞ")
print("Ξ DEFILED Ξ")
print("ΞΞΞΞΞΞΞΞΞΞΞ\n")

# Modes
if args.generate != False:
    print("Running key generator...")
    generate_hashfiles(str(args.generate))

elif args.encrypt != False and args.decrypt != False:
    validate_file(args.encrypt, os.R_OK)
    validate_file(args.decrypt, os.R_OK)
    validate_file(args.file, os.R_OK)
    print("Running verifier...")
    verify(args.encrypt, args.decrypt, args.file)

elif args.encrypt != False:
    validate_file(args.encrypt, os.R_OK)
    validate_file(args.file, os.R_OK)
    print("Running encryptor...")
    encrypt_file(args.encrypt, args.file)

elif args.decrypt != False:
    validate_file(args.decrypt, os.R_OK)
    validate_file(args.file, os.R_OK)
    print("Running decryptor...")
    decrypt_file(args.decrypt, args.file)

else:
    print("Use --help to view usage.")

# Done!
print("Goodbye!")