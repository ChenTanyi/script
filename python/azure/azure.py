#!/usr/bin/env python3
import os
import sys
import jwt
import json
import uuid
import base64
import hashlib
import logging
import datetime
import requests
import urllib3
import OpenSSL.crypto

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

endpoint = 'https://login.microsoftonline.com/{tenant_id}/oauth2/token'


def sign_jwt(tenant_id, client_id, certificate_file) -> str:
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(minutes = 10)

    with open(certificate_file, 'rb') as fin:
        private_key_bytes = fin.read()
    cert = OpenSSL.crypto.dump_certificate(
        OpenSSL.crypto.FILETYPE_ASN1,
        OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM,
            private_key_bytes,
        ),
    )
    fingerprint = hashlib.sha1(cert).digest()
    header = {
        'alg': 'RS256',
        'typ': 'JWT',
        'x5t': base64.b64encode(fingerprint).decode('utf-8'),
    }
    payload = {
        'aud': endpoint.format(tenant_id = tenant_id),
        'iss': client_id,
        'sub': client_id,
        'jti': str(uuid.uuid4()),
        'nbf': int(now.timestamp()),
        'exp': int(expire.timestamp()),
    }

    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.backends import default_backend
        private_key = serialization.load_pem_private_key(
            private_key_bytes, password = None, backend = default_backend())
    except:
        private_key = private_key_bytes
    return jwt.encode(payload, private_key, 'RS256', header)


def request_token():
    auth_file = os.environ.get('AZURE_AUTH_LOCATION')
    client_id = None
    client_secret = None
    tenant_id = None

    if not auth_file or not os.path.exists(auth_file):
        tenant_id = os.environ.get("AZURE_TENANT_ID")
        client_id = os.environ.get("AZURE_CLIENT_ID")
        client_secret = os.environ.get("AZURE_CLIENT_SECRET")
        client_certificate = os.environ.get("AZURE_CLIENT_CERTIFICATE")
        if not tenant_id or not client_id or not (client_secret or
                                                  client_certificate):
            logging.error(
                'Cannot get AZURE_AUTH_LOCATION or AZURE_TENANT_ID and AZURE_CLIENT_ID and AZURE_CLIENT_SECRET/AZURE_CLIENT_CERTIFICATE'
            )
            sys.exit(1)
    else:
        with open(auth_file) as fin:
            azure_auth = json.load(fin)
        tenant_id = azure_auth.get('tenantId')
        client_id = azure_auth.get('clientId')
        client_secret = azure_auth.get('clientSecret')
        client_certificate = azure_auth.get('clientCertificate')
        if client_certificate:
            client_certificate = os.path.join(
                os.path.abspath(os.path.dirname(auth_file)), client_certificate)

    body = {
        'resource': 'https://management.azure.com/',
        'client_info': 1,
        'grant_type': 'client_credentials',
    }
    if client_secret:
        body['client_id'] = client_id
        body['client_secret'] = client_secret
    elif client_certificate:
        body[
            'client_assertion_type'] = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
        body['client_assertion'] = sign_jwt(tenant_id, client_id,
                                            client_certificate)
    else:
        logging.error('Cannot get clientSecret or clientCertificate')
        sys.exit(1)

    r = requests.post(
        endpoint.format(tenant_id = tenant_id),
        data = body,
        verify = True,
    )

    if r.status_code >= 400:
        logging.error(
            f'{r.request.method} {r.url} {r.status_code}: {r.content}')
        sys.exit(1)

    return r.json()


def print_subs(token):
    r = requests.get(
        'https://management.azure.com/subscriptions?api-version=2020-01-01',
        headers = {'Authorization': f'Bearer {token}'},
        verify = True,
    )

    if r.status_code >= 400:
        logging.error(
            f'{r.request.method} {r.url} {r.status_code}: {r.content}')
        sys.exit(1)

    for sub in r.json()['value']:
        print(sub['subscriptionId'], sub['displayName'])


def main(argv):
    token = request_token()['access_token']
    print(token)
    print_subs(token)
    if 'win' in sys.platform:
        os.system(f'echo {token} | clip')


if __name__ == "__main__":
    logging.basicConfig(format = '%(asctime)s %(levelname)s %(message)s')
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    main(sys.argv)