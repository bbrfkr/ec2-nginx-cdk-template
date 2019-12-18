#!/bin/sh -xe

envsubst \
  '$TARGET_HOST$RESOLVER_IP' \
  < /etc/nginx/conf.d/http.conf.template \
  > /etc/nginx/conf.d/http.conf
