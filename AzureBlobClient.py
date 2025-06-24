import os
from azure.storage.blob import BlobServiceClient

# Configuration
# set this via export from local 
#AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=your_account_name;AccountKey=your_key;EndpointSuffix=core.windows.net"
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "your-container-name"

# Initialize the client
blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Ensure the container exists
try:
    container_client.get_container_properties()
except Exception:
    container_client.create_container()

def upload_all_files_in_folder(local_folder_path):
    print(f"\nUploading files from: {local_folder_path}")
    for root, dirs, files in os.walk(local_folder_path):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            blob_name = os.path.relpath(full_path, local_folder_path).replace("\\", "/")  # Preserve folder structure
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
    local_upload_folder = "path/to/local/upload_folder"
    local_download_folder = "path/to/local/download_folder"

    upload_all_files_in_folder(local_upload_folder)
    download_all_blobs_to_folder(local_download_folder)
