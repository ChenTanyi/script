#!/usr/bin/env python3
import os
import sys
import json
import logging
import OpenSSL

def generate_pfx():
    pkey = OpenSSL.crypto.PKey()
    pkey.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    cert = OpenSSL.crypto.X509()
    cert.set_serial_number(0)
    cert.get_subject().CN = 'me'
    cert.set_issuer(cert.get_subject())
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_pubkey(pkey)
    cert.sign(pkey, 'md5')

    pfx = OpenSSL.crypto.PKCS12()
    pfx.set_privatekey(pkey)
    pfx.set_certificate(cert)
    
    return pfx

def main():
    pfx = generate_pfx()
    open('test.pfx', 'wb').write(pfx.export())

if __name__ == "__main__":
    main()