#!/usr/bin/env python3
import os

host = "management.azure.com"
subscription = "" or os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group = ""
container_app = ""
api_version = "2022-01-01-preview"

LOCATION = ""
ENV_ID = ""
REQ_PATH = ""
UUID = ""

url = f"https://{host}/subscriptions/{subscription}/resourcegroups/{resource_group}/providers/Microsoft.App/containerApps/{container_app}?api-version={api_version}"
body = {
    "location": f"{LOCATION}",
    "properties": {
        "managedEnvironmentId": f"{ENV_ID}",
        "configuration": {
            "activeRevisionsMode": "single",
            "ingress": {
                "external": True,
                "targetPort": 80,
                "transport": "auto",
                "allowInsecure": False,
            }
        },
        "template": {
            "containers": [{
                "name":
                    "v2proxy",
                "image":
                    "chentanyi/v2proxy:latest",
                "command": [],
                "args": [],
                "resources": {
                    "cpu": ".25",
                    "memory": ".5Gi"
                },
                "env": [{
                    "name": "REQ_PATH",
                    "value": f"{REQ_PATH}",
                }, {
                    "name": "UUID",
                    "value": f"{UUID}",
                }],
            }],
            "scale": {
                "minReplicas": 0,
                "maxReplicas": 1
            },
        }
    }
}