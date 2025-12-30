# 0. Create Secrets
kubectl create secret generic postgres-secret \
  --from-literal=POSTGRES_USER=psql_user \
  --from-literal=POSTGRES_PASSWORD=psql_password \
  --from-literal=POSTGRES_HOST=postgres \
  --from-literal=POSTGRES_PORT=5432 \
  --from-literal=DATABASE=postgres \
  -n fastapi-app

# 1. Use Docker Minikube
eval $(minikube docker-env)

# 2. Build local backend image if need
docker build -t backend:latest .

# if dockerhub
docker tag localhost/image_name:v1 username/image_name:v1
docker push username/image_name:v1


# 3. Create namespace
kubectl apply -f k8s/namespace.yaml

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



### for macos
docker tag localhost/backend:latest backend:latest # alias