# 1.1. Use Docker Minikube (optinal)
eval $(minikube docker-env)

# 1.2. Build local backend image and push to docker hub
## linux
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap
# create image and push it to docker hub 
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t <YOUR_DOCKERHUB_USERNAME>/test_fastapi_kuber_async_backend:v1 \
  --push .

## macos
- podman manifest create docker.io/<YOUR_DOCKERHUB_USERNAME>/test_fastapi_kuber_async_backend:v1
- podman build \
  --platform linux/amd64 \
  -t test_fastapi_kuber_async_backend:amd64 .
- podman build \
  --platform linux/arm64 \
  -t test_fastapi_kuber_async_backend:arm64 .
- podman manifest add docker.io/<YOUR_DOCKERHUB_USERNAME>/test_fastapi_kuber_async_backend:v1 \
  test_fastapi_kuber_async_backend:amd64
- podman manifest add docker.io/<YOUR_DOCKERHUB_USERNAME>/test_fastapi_kuber_async_backend:v1 \
  test_fastapi_kuber_async_backend:arm64
- podman manifest push \
  docker.io/<YOUR_DOCKERHUB_USERNAME>/test_fastapi_kuber_async_backend:v1

# 2. Create namespace
kubectl apply -f k8s/namespace.yaml


# 3. Create secretes
kubectl create secret generic postgres-secret \
  --from-literal=POSTGRES_USER=psql_user \
  --from-literal=POSTGRES_PASSWORD=psql_password \
  --from-literal=POSTGRES_HOST=postgres \
  --from-literal=POSTGRES_PORT=5432 \
  --from-literal=DATABASE=postgres \
  -n fastapi-app

# 4. Apply Postgres
kubectl apply -f k8s/postgres/pvc.yaml
kubectl apply -f k8s/postgres/deployment.yaml
kubectl apply -f k8s/postgres/service.yaml

# 5. Check Postgres
kubectl get pods -n fastapi-app -w
kubectl logs deployment/postgres -n fastapi-app

# 6. Apply Backend
kubectl apply -f k8s/backend/deployment.yaml
kubectl apply -f k8s/backend/service.yaml

# 7. Check Backend
kubectl get pods -n fastapi-app -w
kubectl logs deployment/backend -n fastapi-app

# 8. For test in browser
kubectl port-forward svc/backend 8000:8000 -n fastapi-app
