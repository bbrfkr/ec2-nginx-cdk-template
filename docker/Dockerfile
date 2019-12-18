FROM nginx:latest

RUN rm -f /etc/nginx/conf.d/default.conf
COPY docker-entrypoint.sh generate-conf.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh /usr/local/bin/generate-conf.sh

COPY http.conf.template /etc/nginx/conf.d/http.conf.template

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
