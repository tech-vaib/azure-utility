import os
import logging
import requests
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/function")
async def main():
    logging.info('Container App HTTP request received.')

    # Connect to Cosmos DB (Mongo API)
    try:
        cosmos_conn_str = os.getenv('COSMOS_MONGO_CONNECTION_STRING')
        database_name = os.getenv('COSMOS_DATABASE_NAME')
        collection_name = os.getenv('COSMOS_COLLECTION_NAME')

        client = MongoClient(cosmos_conn_str)
        db = client[database_name]
        collection = db[collection_name]

        doc_count = collection.count_documents({})
        logging.info(f"Documents in collection '{collection_name}': {doc_count}")
    except Exception as e:
        logging.error(f"Cosmos DB connection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Cosmos DB connection failed: {e}")

    # Make HTTP POST request
    try:
        post_url = os.getenv('HTTP_POST_URL')
        payload = {"message": "Hello from Container App"}
        response = requests.post(post_url, json=payload)
        logging.info(f"POST to {post_url} status: {response.status_code}")
    except Exception as e:
        logging.error(f"HTTP POST failed: {e}")
        raise HTTPException(status_code=500, detail=f"HTTP POST failed: {e}")

    return JSONResponse(content={
        "document_count": doc_count,
        "http_post_status": response.status_code
    })
