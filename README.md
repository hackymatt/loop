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

Monitoring:
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090 -n monitoring
kubectl port-forward svc/prometheus-grafana 4000:80 -n monitoring
