FROM nginx:1.17-alpine

RUN rm -r /etc/nginx/conf.d/*
ARG ENV
COPY "sites/server-$ENV.conf" "/etc/nginx/conf.d"