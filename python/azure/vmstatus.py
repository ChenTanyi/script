#!/usr/bin/env python3
import sys
import json
import requests

host = 'management.azure.com'

subscriptionId = 'f807a126-d943-40c6-877d-61978770aa19'
resourceGroupName = 'jp'
vmName = 'jp'
operation = sys.argv[2] if len(sys.argv) > 2 else 'deallocate'

path = f'/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/{operation}?api-version=2019-03-01'
url = f'HTTPS://{host}/{path}'

r = requests.post(
    url = url,
    headers = {
        'Authorization': f'Bearer {sys.argv[1]}'
    },
)

print(r.status_code, r.reason)
try:
    print(json.dumps(r.json(), indent=2))
except:
    print(r.content)