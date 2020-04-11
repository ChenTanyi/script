#!/usr/bin/env python3
import os
import sys
import json
import logging
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def request_token():
    auth_file = os.environ.get('AZURE_AUTH_LOCATION')
    client_id = None
    client_secret = None
    tenant_id = None

    if not auth_file or not os.path.exists(auth_file):
        client_id = os.environ.get("AZURE_CLIENT_ID")
        client_secret = os.environ.get("AZURE_CLIENT_SECRET")
        tenant_id = os.environ.get("AZURE_TENANT_ID")
        if not client_id or not client_secret or not tenant_id:
            logging.error(
                'Cannot get AZURE_AUTH_LOCATION or AZURE_CLIENT_ID and AZURE_CLIENT_SECRET and AZURE_TENANT_ID'
            )
            sys.exit(1)
    else:
        azure_auth = json.load(open(auth_file))
        client_id = azure_auth['clientId']
        client_secret = azure_auth['clientSecret']
        tenant_id = azure_auth['tenantId']

    r = requests.post(
        f'https://login.microsoftonline.com/{tenant_id}/oauth2/token',
        data={
            'resource': 'https://management.core.windows.net/',
            'client_id': client_id,
            'client_secret': client_secret,
            'client_info': 1,
            'grant_type': 'client_credentials',
        },
        verify = True)

    return r.json()

def main(argv):
    token = request_token()['access_token']
    print(token)
    if 'win' in sys.platform:
        os.system(f'echo {token} | clip')

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    main(sys.argv)