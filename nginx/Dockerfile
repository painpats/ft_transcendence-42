FROM nginx:latest

RUN apt update -y && apt upgrade -y

RUN mkdir -p /etc/nginx/ssl
RUN apt install openssl -y

COPY script.sh /usr/local/bin/script.sh
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 443

ENTRYPOINT ["bash", "/usr/local/bin/script.sh"]