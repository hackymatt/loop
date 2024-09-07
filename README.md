# loop

Cluster applications:
Cert Manager
Civo cluster autoscaler
Helm
Metrics Server
Nginx
PostgreSQL

Build docker:
docker build -t loopedupl/backend:latest ./backend
docker build -t loopedupl/frontend:latest ./frontend
docker build -t loopedupl/nginx:latest ./nginx

Push docker:
docker push loopedupl/backend:latest
docker push loopedupl/frontend:latest
docker push loopedupl/nginx:latest

Create secrets:
kubectl delete secret secrets
kubectl create secret generic secrets --from-env-file=./secrets.sh

kubectl delete secret auth
kubectl create secret generic auth --from-file=./auth

Delete cert:
kubectl delete cert tls-cert

Deploy:
helm dep update
helm upgrade --install -f values-dev.yaml loop . -n default

cat civo-kubeconfig | base64
