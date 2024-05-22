# loop

Build docker:
docker build -t loopedupl/backend:latest . --file ./backend/Dockerfile
docker build -t loopedupl/frontend:latest . --file ./frontend/Dockerfile
docker build -t loopedupl/nginx:latest . --file ./nginx/Dockerfile

Push docker:
docker push loopedupl/backend:latest
docker push loopedupl/frontend:latest
docker push loopedupl/nginx:latest

Create secrets:

kubectl create secret generic backend-secret --from-env-file=./backend_secrets.sh
kubectl create secret generic email-secret --from-env-file=./email_secrets.sh
kubectl create secret generic facebook-secret --from-env-file=./facebook_secrets.sh
kubectl create secret generic frontend-secret --from-env-file=./frontend_secrets.sh
kubectl create secret generic github-secret --from-env-file=./github_secrets.sh
kubectl create secret generic google-secret --from-env-file=./google_secrets.sh
kubectl create secret generic postgres-secret --from-env-file=./postgres_secrets.sh
