## local build and run

docker build -t my-fastapi-container .
docker run -p 8080:80 my-fastapi-container

curl http://localhost:8080/api/function
# Push image to container registry
docker tag my-fastapi-container <registry-name>.azurecr.io/my-fastapi-container:v1
docker push <registry-name>.azurecr.io/my-fastapi-container:v1

# Deploy to Azure Container Apps
az containerapp create \
  --name my-fastapi-app \
  --resource-group <resource-group> \
  --environment <container-app-env> \
  --image <registry-name>.azurecr.io/my-fastapi-container:v1 \
  --cpu 0.5 --memory 1.0Gi \
  --ingress external --target-port 80 \
  --env-vars COSMOS_MONGO_CONNECTION_STRING="<your-cosmos-conn-string>" \
             COSMOS_DATABASE_NAME="<db-name>" \
             COSMOS_COLLECTION_NAME="<collection-name>" \
             HTTP_POST_URL="https://example.com/api"
