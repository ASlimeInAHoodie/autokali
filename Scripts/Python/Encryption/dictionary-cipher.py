#!/usr/bin/env python
### DICTIONARY CIPHER
## DESCRIPTION:
# This script is an encryption method that uses a dictionary as a key to encrypt a string. This is not
# an original method, but a variation to help improve security. In all techniques, the output is an
# array of locations to where within the dictionary they are held. The start of the encrypted text is
# the formatting used and symbolize how the string was encoded and encrypted. 蘇州碼子 is used as the
# mark for an encrypted string (a reference to my favorite use of the book cipher) and ends with
# 蘇州碼子 once the formatting information is done. See bottom of script for the table of info.
# For the dictionary, you can use the basic built in ASCII or NUMBER dictionary, or you can build one
# using the built-in dictionary builder. You can also make your own as long as it has all the characters
# used in the encryption, duplicate characters will be skipped.
# Different encoding methods can be done to make it more challenging to crack the method including
# encoding to hex or base 64 first. You can also pipe your own encoded string into this file too by
# leaving text empty, however the output will not remember how you have encoded your input. More
# iterations can also be done to add extra encryption. Using non english characters or other format
# characters (such as '\x00' ) as a separator is also a great way to increase encryption.
## ARGUMENTS:
# Args              | Description                                                               | Input     | Defaults
# ----              | ----                                                                      | ----      | ----
# -b, --builder     | Want to create a custom dictionary?                                       | BOOLEAN   | False
# -t, --text        | What is the string to encrypt/decrypt?                                    | STRING    | EMPTY ('')
# -d, --dictionary  | What dictionary to use? (0 for ASCII, 1 for NUMBER, or path of custom)    | STRING    | '0'
# -e, --encoding    | What type of encoding to use (0 for raw, 1 for hex, 2 for base64)         | INT       | 0
# -s, --separator   | How do you want to separate each pointer?                                 | STRING    | ", "
# -i, --iterations  | How many iterations do you want to encrypt with?                          | INT       | 1

## IMPORTS
import binascii
import base64
import random
import argparse
import os

# Arguement parsing
parser = argparse.ArgumentParser( prog='Dictionary Cipher', description='Encrypt a string with a dictionary', epilog='made by ASlimeInAHoodie in VS Code' )
parser.add_argument('-t', '--text', default='')
parser.add_argument('-e', '--encoding', default='0')
parser.add_argument('-s', '--separator', default=', ')
parser.add_argument('-i', '--iterations', default='1')
parser.add_argument('-d', '--dictionary', default='0')
parser.add_argument('-b', '--builder', action='store_true', default=False)


## LOAD AND VALIDATE ARGUMENTS
# Custom error handler
class InputError(Exception):
    pass

# Load args into args variable
args = parser.parse_args()

# Builder validation
launch_builder = args.builder
launch_builder = launch_builder == 'True' or launch_builder == 'true' or launch_builder == 'TRUE' or launch_builder == True

# String validation
input_text = args.text
# If input_text empty then ask for input instead
if (input_text == '' and launch_builder == False):
    print("\n\n\n\n")
    print("ΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞ")
    print("Ξ DICTIONARY Ξ CIPHER Ξ")
    print("ΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞ\n")
    input_text = input("Input encrypted/decrypted text: ")

# Dictionary validation
dictionary = args.dictionary
if ((not launch_builder) and dictionary != '0' and dictionary != '1'):
    if (os.path.exists(dictionary) == False):
        raise InputError("Invalid dictionary (Does not exist)")
    elif (os.access(dictionary, os.R_OK) == False):
        raise InputError("Invalid dictionary (Unable to read file)")

# Encoding validation
encoding_id = args.encoding
try:
    encoding_id = int(encoding_id)
except Exception:
    raise InputError("Invalid encoding id (The encoding id must be an integer)")
if (encoding_id < 0 or encoding_id > 2):
    raise InputError("Invalid encoding id (Encoders are 0 for raw, 1 for hex, and 2 for base64)")

# Separator validation
separator = args.separator
if (separator.isdigit()):
    raise InputError("Invalid separator (An only digits seperator cannot be used)")

# Iterations validator
iterations = args.iterations
try:
    iterations = int(iterations)
except Exception:
    raise InputError("Invalid iteration count (The iteration count must be an integer)")
if (iterations < 1):
    raise InputError("Invalid iteration count (The iteration count cannot be less than 1)")
if (iterations > 16):
    while True:
        print("Ξ HIGH Ξ ITERATION Ξ COUNT Ξ DETECTED Ξ")
        print("More than 16 iterations will not not improve encryption and will eat up more computer resources than necessary.")
        do_continue = input("Are you sure you would like to continue? Y/N ").capitalize()
        if (do_continue == 'Y' or do_continue == 'YES'):
            break
        elif (do_continue == 'N' or do_continue == 'NO'):
            raise InputError("Invalid iteration count (User halted the program)")

## FUNCTIONS
def encrypt(text, dictionary, seperator):
    enc_text = ""
    for i in text:
        enc_text += str(dictionary.find(i)) + seperator
    return enc_text

def decrypt(text, dictionary, seperator):
    dec_text = ""
    for i in text.split(seperator)[:-1]:
        dec_text += dictionary[int(i)]
    return dec_text

def hexxed(text):
    # Hexlify twice to remove all but numbers from the input
    first = (binascii.hexlify(text.encode())).decode()
    second = (binascii.hexlify(first.encode())).decode()
    return second

def unhexxed(text):
    # Unhexlify twice as per hexxed function
    first = (binascii.unhexlify(text.encode())).decode()
    second = (binascii.unhexlify(first)).decode()
    return second

def based(text):
    # Base64 encode
    first = (base64.b64encode(text.encode())).decode()
    return first

def unbased(text):
    # Opposite of based
    first = (base64.b64decode(text.encode())).decode()
    return first

## DICTIONARIES
# Basic Dictionaries
NUMBER = 1234567890
ASCII = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_-+={[]}\|;:',<.>/? " + '"'
# Set Dictionary
if (dictionary == '0'):
    dictionary = ASCII
elif (dictionary == '1'):
    dictionary = NUMBER
# Dictionary Builder
while launch_builder:
    print("\n\n\n\n\n\n\n\n")
    print("ΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞ")
    print("Ξ Dictionary Ξ Builder Ξ")
    print("ΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞΞ")
    print("\n\n")
    print("Select from the list below for which character you would like. The order you put the")
    print("characters in will be the order that the final dictionary comes out with.")
    print("r = RANDOM-ORDER, a = ASCII, l = LOWERCASE, u = UPPERCASE, n = NUMBERS, s = SYMBOLS, ! = NOSPACES")
    get_symbols = input("Which character structure would you like? ").lower()
    # Check random
    use_random = False
    if 'r' in get_symbols: use_random = True
    get_symbols.replace('r', '')
    # Check all ascii
    use_all = False
    if 'a' in get_symbols: use_all = True
    get_symbols.replace('a', '')

    symbols = list(get_symbols)

    dictionary_text = ''
    characters = ' '

    if use_all: characters = ASCII

    if not use_all:
        for i in symbols:
            if (i == 'l'): characters += "abcdefghijklmnopqrstuvwxyz"
            if (i == 'u'): characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if (i == 'n'): characters += "1234567890"
            if (i == 's'): characters += "~`!@#$%^&*()_-+={[]}\|;:',<.>/?" + '"'

    if use_random: characters = ''.join(random.sample(characters, len(characters)))
    while launch_builder:
        print("\n\n\n\n")
        print("Ξ Dictionary Built Ξ")
        print("Your dictionary is: " + characters)
        get_save = input("Save to file? Y/N ").capitalize()
        print(get_save)
        if (get_save == 'N' or get_save == 'NO'):
            print("Bye bye.")
            raise SystemExit(0)
        elif (get_save == 'Y' or get_save == 'YES'):
            while launch_builder:
                get_file = input("Path to save file to? ")
                if (os.path.exists(get_file) and os.access(get_file, os.W_OK) == False):
                    print("Invalid path (Unable to write to file)")
                    OutFile = False
                elif (os.path.exists(get_file) == False):
                    OutFile = open(get_file, "x")
                else:
                    OutFile = open(get_file, "w")
                if (OutFile != False):
                    OutFile.write(characters)
                    OutFile.close()
                    print("Saved to file. Goodbye now.")
        else:
            print("Invalid option")

## DECRYPTION
if input_text.startswith("蘇州碼子"):
    print("Ξ ENCRYPTED Ξ STRING Ξ IDENTIFIED Ξ")
    # Get the arguments, output should be [ENCODING, ITERATIONS, SEPERATOR]
    encoding_id = int(input_text.split("蘇州碼子")[1].split('〇')[1].split('〺')[0])
    iterations = int(input_text.split("蘇州碼子")[1].split('〇')[1].split('〺')[1].split('〹')[0])
    separator = str(input_text.split("蘇州碼子")[1].split('〇')[1].split('〺')[1].split('〹')[1])
    enc_text = input_text.split("蘇州碼子")[2]
    print("Ξ Decoding Format: " + ["RAW", "HEX", "BASE64"][encoding_id] + " encoding, " + str(iterations) + " iterations, and '" + separator + "' separator..")
    dec_text = decrypt(enc_text, dictionary, separator)
    if (encoding_id == 1):
        # Convert to hex
        dec_text = unhexxed(dec_text)
    elif (encoding_id == 2):
        # Convert to base64
        dec_text = unbased(dec_text)
    elif (encoding_id != 0):
        raise InputError("Sorry! Something went wrong!")
    print(dec_text)
## ENCRYPTION
else:
    enc_text = input_text
    prefix = "蘇州碼子"
    if (encoding_id == 0):
        # Do nothing as raw
        prefix += "〇0"
    elif (encoding_id == 1):
        # Convert to hex
        enc_text = hexxed(enc_text)
        prefix += "〇1"
    elif (encoding_id == 2):
        # Convert to base64
        enc_text = based(enc_text)
        prefix += "〇2"
    else:
        raise InputError("Sorry! Something went wrong!")
    for i in range(iterations):
        enc_text = encrypt(enc_text, dictionary, separator)
    prefix += "〺" + str(iterations) + "〹" + separator + "〹蘇州碼子"
    print(prefix + enc_text)
    
## TABLE OF INFORMATION - Suzhou Numeral System
# 蘇州碼子      = Start/End of formatting
# 〇<INT>       = Encoding, <INT> is id: 0 = raw, 1 = Hex, 2 = Base64
# 〺<INT>       = Iterations, <INT> number of times
# 〹<STRING>〹  = Seperator, <STRING> is the seperator
