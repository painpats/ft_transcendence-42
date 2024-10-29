#!/bin/bash

openssl req -x509 -nodes -out $NGINX_CRT -keyout $NGINX_KEY -subj $NGINX_SUB

exec nginx -g 'daemon off;'