import logging
import os
import requests
from pymongo import MongoClient
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Function started.')

    # 1. Connect to Cosmos DB (Mongo API)
    try:
        cosmos_conn_str = os.getenv('COSMOS_MONGO_CONNECTION_STRING')
        database_name = os.getenv('COSMOS_DATABASE_NAME')
        collection_name = os.getenv('COSMOS_COLLECTION_NAME')

        client = MongoClient(cosmos_conn_str)
        db = client[database_name]
        collection = db[collection_name]

        # Simple operation: count documents
        doc_count = collection.count_documents({})
        logging.info(f"Documents in collection '{collection_name}': {doc_count}")
    except Exception as e:
        logging.error(f"Cosmos DB connection failed: {e}")
        return func.HttpResponse(f"Cosmos DB connection failed: {e}", status_code=500)

    # 2. Make an HTTP POST request to external service
    try:
        post_url = os.getenv('HTTP_POST_URL')
        payload = {"message": "Hello from Azure Function in Cosmos DB env"}
        response = requests.post(post_url, json=payload)
        logging.info(f"POST to {post_url} status: {response.status_code}")
    except Exception as e:
        logging.error(f"HTTP POST failed: {e}")
        return func.HttpResponse(f"HTTP POST failed: {e}", status_code=500)

    return func.HttpResponse(
        f"Document count: {doc_count}\nHTTP POST Status: {response.status_code}"
    )
