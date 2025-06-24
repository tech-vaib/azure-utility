import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Replace with your Azure Storage Account URL
STORAGE_ACCOUNT_URL = "https://<your-storage-account-name>.blob.core.windows.net"
CONTAINER_NAME = "your-container-name"

# Use managed identity / Azure AD for authentication
credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=credential)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Ensure container exists or create it
try:
    container_client.get_container_properties()
except Exception:
    container_client.create_container()

def upload_all_files_in_folder(local_folder_path):
    print(f"\nUploading files from: {local_folder_path}")
    for root, dirs, files in os.walk(local_folder_path):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            blob_name = os.path.relpath(full_path, local_folder_path).replace("\\", "/")  # Use forward slashes for blob naming
            blob_client = container_client.get_blob_client(blob_name)
            with open(full_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"Uploaded: {blob_name}")

def download_all_blobs_to_folder(destination_folder_path):
    print(f"\nDownloading files to: {destination_folder_path}")
    blobs = container_client.list_blobs()
    for blob in blobs:
        blob_client = container_client.get_blob_client(blob)
        download_path = os.path.join(destination_folder_path, blob.name.replace("/", os.sep))
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        with open(download_path, "wb") as file:
            file.write(blob_client.download_blob().readall())
        print(f"Downloaded: {blob.name} to {download_path}")

# Example usage
if __name__ == "__main__":
    upload_folder = "path/to/local/upload_folder"
    download_folder = "path/to/local/download_folder"

    upload_all_files_in_folder(upload_folder)
    download_all_blobs_to_folder(download_folder)
