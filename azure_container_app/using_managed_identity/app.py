import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from pymongo import MongoClient

app = FastAPI()

@app.get("/api/function")
async def main():
    logging.info("Request received.")

    # Blob Storage access with Managed Identity
    try:
        blob_account_url = os.getenv("BLOB_ACCOUNT_URL")  # e.g. https://<account>.blob.core.windows.net
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url=blob_account_url, credential=credential)
        containers = list(blob_service_client.list_containers())
        container_names = [c.name for c in containers]
    except Exception as e:
        logging.error(f"Blob error: {e}")
        raise HTTPException(status_code=500, detail=f"Blob error: {e}")

    # Cosmos DB access via connection string (AD auth optional)
    try:
        cosmos_conn = os.getenv("COSMOS_MONGO_CONNECTION_STRING")
        db_name = os.getenv("COSMOS_DATABASE_NAME")
        col_name = os.getenv("COSMOS_COLLECTION_NAME")

        client = MongoClient(cosmos_conn)
        collection = client[db_name][col_name]
        doc_count = collection.count_documents({})
    except Exception as e:
        logging.error(f"Cosmos DB error: {e}")
        raise HTTPException(status_code=500, detail=f"Cosmos DB error: {e}")

    return JSONResponse(content={
        "blob_containers": container_names,
        "document_count": doc_count
    })
