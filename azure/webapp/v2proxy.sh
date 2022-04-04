#!/bin/bash
set -e

# Simply create an Azure Web App with v2proxy (UUID is required, REQ_PATH is optional)

RESOURCE_GROUP=""
APPSERVICE_PLAN=""
WEBAPP=""
UUID=""
REQ_PATH=""

# if no resource group and app service plan, uncomment the following command
# az group create -n "$RESOURCE_GROUP" -l eastus
# az appservice plan create -n "$APPSERVICE_PLAN" -g "$RESOURCE_GROUP" --sku B1 --is-linux

az webapp create -n "$WEBAPP" -g "$RESOURCE_GROUP" -p "$APPSERVICE_PLAN" -i chentanyi/v2proxy
az webapp update -n "$WEBAPP" -g "$RESOURCE_GROUP" --https-only
az webapp config appsettings set -n "$WEBAPP" -g "$RESOURCE_GROUP" --settings UUID="$UUID"
az webapp config appsettings set -n "$WEBAPP" -g "$RESOURCE_GROUP" --settings REQ_PATH="$REQ_PATH"
