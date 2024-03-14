#!/bin/sh

cp /usr/share/nginx/html/config.template.js /usr/share/nginx/html/config.js

sed -i "s|{{REACT_APP_BACKEND_IP}}|$REACT_APP_BACKEND_IP|g" /usr/share/nginx/html/config.js

nginx -g 'daemon off;'