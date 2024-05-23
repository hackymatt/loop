FROM nginx:alpine

RUN mkdir -p /etc/nginx/conf.d/
RUN rm /etc/nginx/conf.d/*
COPY default.conf /etc/nginx/conf.d/

# Used for testing ssl/https locally - certs for this website via cloudflare
# more on SSL/HTTPS later
ADD ./certificate/ca.crt /etc/pki/tls/certs/server.crt
ADD ./certificate/ca.key /etc/pki/tls/certs/server.key

EXPOSE 80
EXPOSE 443


CMD [ "nginx", "-g", "daemon off;" ]