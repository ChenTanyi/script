#!/usr/bin/env python3
import sys
import json
import requests
import time
import random
import string

host = 'management.azure.com'

def request(method, path, body, second, url = None):
    time.sleep(second)
    if not url:
        url = f'https://{host}/{path}'
    r = requests.request(
        method = method,
        url = url,
        headers = {
            'Authorization': f'Bearer {sys.argv[1]}'
        },
        json = body,
        timeout = 20,
    )

    print(r.headers)
    print(r.status_code, r.reason)
    return r

# Cost

subscriptionId = 'f807a126-d943-40c6-877d-61978770aa19'
api_version = '2019-11-01'
path = f'/subscriptions/{subscriptionId}/providers/Microsoft.CostManagement/query?api-version={api_version}'
body = {
  "type": "Usage",
  "timeframe": "ThisBilingMonth",
  "dataset": {
    "granularity": "None",
    "aggregation": {
      "totalCost": {
        "name": "PreTaxCost",
        "function": "Sum"
      }
    },
    "grouping": [
      {
        "type": "Dimension",
        "name": "SubscriptionName"
      }
    ]
  }
}

r = request("POST", path, body, 0)
print(json.dumps(r.json(), indent=2))