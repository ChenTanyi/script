#!/bin/bash
set -e

# Simply create an Azure Web App with qBittorrent (only can download due to incoming TCP/UDP connection would be blocked)

RESOURCE_GROUP=""
APPSERVICE_PLAN=""
WEBAPP=""
STORAGE_ACCOUNT=""

# if no resource group and app service plan, uncomment the following command
# az group create -n "$RESOURCE_GROUP" -l eastus
# az appservice plan create -n "$APPSERVICE_PLAN" -g "$RESOURCE_GROUP" --sku B1 --is-linux

az storage account create -n "$STORAGE_ACCOUNT" -g "$RESOURCE_GROUP"
STORAGE_KEY=$(az storage account keys list -n "$STORAGE_ACCOUNT" -g "$RESOURCE_GROUP" --query "[0].value" -o tsv)
FILE_ENDPOINT=$(az storage account show -n "$STORAGE_ACCOUNT" -g "$RESOURCE_GROUP" --query "primaryEndpoints.file" -o tsv)
STORAGE_CONNSTR=$(az storage account show-connection-string -n "$STORAGE_ACCOUNT" -g "$RESOURCE_GROUP" --file-endpoint "$FILE_ENDPOINT" --query "connectionString" -o tsv)
az storage share create -n qbit --connection-string "$STORAGE_CONNSTR" --quota 128
az storage share create -n qbit-config --connection-string "$STORAGE_CONNSTR" --quota 1

FILE_HOST=${FILE_ENDPOINT#https://}
FILE_HOST=${FILE_HOST%/}
FILE_HOST_IP=$(dig +short "$FILE_HOST" | tail -1)
envsubst < qbit.template.yml > docker-compose.yml

# az webapp create -n "$WEBAPP" -g "$RESOURCE_GROUP" -p "$APPSERVICE_PLAN" -i wernight/qbittorrent
# az webapp config appsettings set -n "$WEBAPP" -g "$RESOURCE_GROUP" --settings WEBSITES_PORT=8080
# az webapp config storage-account add -g "$RESOURCE_GROUP" -n "$WEBAPP" -a "$STORAGE_ACCOUNT" -k "$STORAGE_KEY" -i qbit -t AzureFiles --sn qbit -m /downloads
# az webapp config storage-account add -g "$RESOURCE_GROUP" -n "$WEBAPP" -a "$STORAGE_ACCOUNT" -k "$STORAGE_KEY" -i qbit-config -t AzureFiles --sn qbit-config -m /config
# az webapp config storage-account list -g "$RESOURCE_GROUP" -n "$WEBAPP" -o json

az webapp create -n "$WEBAPP" -g "$RESOURCE_GROUP" -p "$APPSERVICE_PLAN" --multicontainer-config-type compose --multicontainer-config-file docker-compose.yml

az webapp update -n "$WEBAPP" -g "$RESOURCE_GROUP" --https-only
