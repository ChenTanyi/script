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
az storage share create -n qbit --account-name "$STORAGE_ACCOUNT" --account-key "$STORAGE_KEY" --quota 128
az storage share create -n qbit-config --account-name "$STORAGE_ACCOUNT" --account-key "$STORAGE_KEY" --quota 1

az webapp create -n "$WEBAPP" -g "$RESOURCE_GROUP" -p "$APPSERVICE_PLAN" -i wernight/qbittorrent
az webapp update -n "$WEBAPP" -g "$RESOURCE_GROUP" --https-only
az webapp config appsettings set -n "$WEBAPP" -g "$RESOURCE_GROUP" --settings WEBSITES_PORT=8080
az webapp config storage-account add -g "$RESOURCE_GROUP" -n "$WEBAPP" -a "$STORAGE_ACCOUNT" -k "$STORAGE_KEY" -i qbit -t AzureFiles --sn qbit -m /downloads
az webapp config storage-account add -g "$RESOURCE_GROUP" -n "$WEBAPP" -a "$STORAGE_ACCOUNT" -k "$STORAGE_KEY" -i qbit-config -t AzureFiles --sn qbit-config -m /config

az webapp config storage-account list -g "$RESOURCE_GROUP" -n "$WEBAPP" -o json
