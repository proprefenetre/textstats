FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

ADD sites-enabled/nginx.conf /etc/nginx/conf.d/default.conf

RUN export DOMAIN="0.0.0.0" && \
    envsubst < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf
