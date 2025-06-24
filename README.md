# azure-utility

## Install the Azure Blob Storage SDK:
pip install azure-storage-blob

export AZURE_STORAGE_CONNECTION_STRING="your-connection-string"

## using identity

pip install azure-identity azure-storage-blob

az role assignment create \
  --assignee <client-id-or-object-id-of-managed-identity> \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-account>