#!/usr/bin/env python
### ID_RSA.PUB-RECON
## DESCRIPTION:
# This script outputs n, p, & q, of weak public RSA id keys. Shoutout to murtaza-u's Fermat's
# Factorization Method in python for the code used to find p & q in this script.
# To reemphasize: This is only for __WEAK__ public keys. Good luck breaking anything strong
# with this.
## ARGUMENTS:
# Args      | Description                                       | Input     | Defaults
# ----      | ----                                              | ----      | ----
# file      | Where is the public id_rsa file?                  | FILE      | NONE - REQUIRED
# digits    | How many digits do you want to see? (0 for all)   | INT       | 0 (INT)
# private   | Do you want to print the private key?             | BOOLEAN   | False (BOOLEAN)

## IMPORTS
import argparse
from Crypto.PublicKey import RSA
from gmpy2 import isqrt

# Arguement parsing
parser = argparse.ArgumentParser( prog='ID_RSA.PUB-RECON', description='print the n, p & q of a public RSA id', epilog='made by ASlimeInAHoodie in VS Code' )
parser.add_argument('file')
parser.add_argument('-d', '--digits', default=0)
parser.add_argument('-p', '--private', default=False)

# Load args into args variable
args = parser.parse_args()

public_rsa = args.file
digits = int(args.digits)
do_printkey = (args.private == "True" or args.private == "TRUE" or args.private == "true")

# Read the public key file
with open(public_rsa, 'r') as file:
    public_key_data = file.read()

# Load the RSA public key
rsa_key = RSA.importKey(public_key_data)

# Get the modulus as an integer
n = rsa_key.n
e = rsa_key.e

print(f"e = {e}")

if (digits <= 0):
    print (f"n = {n}")
else:
    # Calculate the last digits of n
    last_digits = n % 10**digits
    print (f"Last {digits} digits of n = {last_digits}")

# Fermat's Factorization Method
def factorize(n):
    # since even nos. are always divisible by 2, one of the factors will
    # always be 2
    if (n & 1) == 0:
        return (n/2, 2)

    # isqrt returns the integer square root of n
    a = isqrt(n)

    # if n is a perfect square the factors will be ( sqrt(n), sqrt(n) )
    if a * a == n:
        return a, a

    while True:
        a = a + 1
        bsq = a * a - n
        b = isqrt(bsq)
        if b * b == bsq:
            break

    return a + b, a - b

pq = factorize(n)

if (digits <= 0):
    print(f"p = {pq[0]}")
    print(f"q = {pq[1]}")
else:
    last_digits = pq[0] % 10**digits
    print (f"Last {digits} digits of p = {last_digits}")
    last_digits = pq[1] % 10**digits
    print (f"Last {digits} digits of q = {last_digits}")

# Generate private key
if do_printkey:
    from Crypto.Util.number import inverse
    d = inverse(e, (pq[0]-1) * (pq[1]-1))
    rsa_key = RSA.construct((int(n), int(e), int(d), int(pq[0]), int(pq[1])))
    private_key = rsa_key.exportKey()
    print("Private Key:")
    print(private_key.decode())