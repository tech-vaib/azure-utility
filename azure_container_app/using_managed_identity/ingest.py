import os
import logging
from azure.storage.blob import BlobServiceClient
from pymongo import MongoClient, UpdateOne
from typing import List
import json

# Placeholder embedding function — replace with your actual embedding model/service call
def generate_embedding(text: str) -> List[float]:
    # TODO: call your embedding API here
    return [0.0] * 768  # dummy vector

# Simple chunker - split text into chunks of max N characters with overlap
def chunk_text(text: str, chunk_size=500, overlap=50) -> List[str]:
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def main():
    logging.basicConfig(level=logging.INFO)
    env = os.getenv("ENVIRONMENT", "dev").lower()
    logging.info(f"Running ingestion in '{env}' environment")

    # Load env vars
    blob_conn_str = os.getenv(f"BLOB_CONNECTION_STRING_{env.upper()}")
    cosmos_conn_str = os.getenv(f"COSMOS_CONN_STRING_{env.upper()}")
    blob_container = os.getenv(f"BLOB_CONTAINER_{env.upper()}", f"data-{env}")

    if not all([blob_conn_str, cosmos_conn_str]):
        logging.error("Missing connection strings for Blob or Cosmos DB")
        return

    # Connect to Blob Storage
    blob_service = BlobServiceClient.from_connection_string(blob_conn_str)
    container_client = blob_service.get_container_client(blob_container)

    # Connect to Cosmos DB (Mongo API)
    mongo_client = MongoClient(cosmos_conn_str)
    db = mongo_client["rag_database"]
    collection = db["embeddings"]

    # List blobs
    blobs = container_client.list_blobs()
    for blob in blobs:
        logging.info(f"Processing blob: {blob.name}")
        blob_client = container_client.get_blob_client(blob)
        data = blob_client.download_blob().readall()
        
        # Assuming text files, decode
        try:
            text = data.decode("utf-8")
        except Exception as e:
            logging.warning(f"Skipping blob {blob.name}, cannot decode: {e}")
            continue

        chunks = chunk_text(text)

        # Prepare bulk ops for upsert
        operations = []
        for i, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)
            doc_id = f"{blob.name}_chunk_{i}"
            operations.append(UpdateOne(
                {"_id": doc_id},
                {"$set": {
                    "text": chunk,
                    "embedding": embedding,
                    "source_blob": blob.name,
                    "chunk_index": i,
                }},
                upsert=True
            ))
        
        if operations:
            result = collection.bulk_write(operations)
            logging.info(f"Upserted {result.upserted_count + result.modified_count} chunks from {blob.name}")

    logging.info("Ingestion complete")

if __name__ == "__main__":
    main()
