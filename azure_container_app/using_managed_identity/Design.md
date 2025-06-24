1. Overview

This pipeline ingests raw data files stored in Azure Blob Storage, processes these files in a Python application running as an Azure Container App, generating chunked embeddings, and stores/upserts them in Cosmos DB (Mongo API). The pipeline supports multiple environments (dev, stage, prod) and is triggered manually via GitHub Actions.

2. Architecture Diagram
+-------------------------+
|    Azure Blob Storage    |
| (Data files: PDFs, CSVs,|
|  JSON, TXT, etc.)        |
+------------+------------+
             |
             | (Blob SDK, Managed Identity)
             v
+-------------------------+
|   Azure Container App   |  <-- Runs Python ingestion service
|  (Python app with FastAPI|
|   or script)             |
+------------+------------+
             |
             | (Mongo Driver)
             v
+-------------------------+
| Cosmos DB (Mongo API)   |
| (Embedding vector store)|
+-------------------------+

          ^                      
          |                      
+-------------------------+
|    GitHub Actions       |
| - Manual trigger        |
| - Deploy & run pipeline |
| - Set environment       |
+-------------------------+

3. Components & Responsibilities
3.1 Azure Blob Storage

    Stores all raw data files to ingest.

    Accessed securely by Container App via Managed Identity or connection string.

3.2 Azure Container App

    Hosts the Python ingestion service.

    On trigger, runs the pipeline:

        Loads files from Blob Storage.

        Splits documents into chunks.

        Generates embeddings (OpenAI, HuggingFace, etc.).

        Upserts embeddings into Cosmos DB.

    Configured with environment-specific variables (blob container, Cosmos connection string, embedding API key).

    Can expose an HTTP endpoint for manual/automated triggers or be triggered by GitHub Actions directly.

3.3 Cosmos DB (Mongo API)

    Stores document chunks and embeddings.

    Used later for semantic search or retrieval.

3.4 GitHub Actions

    Automates deployment of Container App per environment.

    Allows manual triggering of the ingestion pipeline.

    Injects secrets and environment variables.

    Supports three environments: dev, stage, prod.

4. Workflow

    Deployment:

        GitHub Actions workflow deploys or updates the Azure Container App for the chosen environment (dev, stage, or prod).

        Environment-specific secrets and config are set.

    Trigger:

        Manual trigger of GitHub Actions workflow to run the ingestion.

        Workflow calls the Container App’s ingestion endpoint or runs a command inside the Container App (e.g., Azure CLI or REST call).

    Ingestion:

        Container App’s Python app:

            Reads files from Azure Blob Storage.

            Chunks and embeds them.

            Upserts into Cosmos DB.

    Completion:

        Logs and success status returned to GitHub Actions.

        Errors surfaced in workflow logs.

5. Environment Configuration
Environment	Blob Container	Cosmos DB Connection String	Embedding API Key
dev	data-dev	COSMOS_CONN_STRING_DEV	EMBEDDING_API_KEY_DEV
stage	data-stage	COSMOS_CONN_STRING_STAGE	EMBEDDING_API_KEY_STAGE
prod	data-prod	COSMOS_CONN_STRING_PROD	EMBEDDING_API_KEY_PROD

Each environment has its own set of secrets stored securely in GitHub and Azure.
6. Security

    Use Managed Identities to allow Container App access to Blob Storage and Cosmos DB securely.

    Secrets (embedding API keys, Cosmos connection strings) stored in GitHub Secrets and injected at runtime.

    Role assignments in Azure ensure least privilege.

7. Deployment and Triggering via GitHub Actions

    Workflow supports:

        Deploying/updating Container App with environment-specific settings.

        Manually triggering the ingestion pipeline by sending a request to the Container App endpoint.

    Use workflow inputs for selecting environment.