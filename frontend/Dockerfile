FROM node:24-alpine AS development
WORKDIR /workspace/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

FROM development AS build
ARG PUBLIC_BASE=/
ARG API_BASE=
ENV VITE_PUBLIC_BASE=${PUBLIC_BASE} \
    VITE_API_BASE=${API_BASE}
WORKDIR /workspace
COPY app/static/ ./app/static/
COPY demo/patron-topografico.svg ./demo/patron-topografico.svg
COPY frontend/ ./frontend/
WORKDIR /workspace/frontend
RUN npm run build

FROM nginxinc/nginx-unprivileged:1.28-alpine AS production
COPY deploy/nginx/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /workspace/frontend/dist/ /usr/share/nginx/html/
ENV API_UPSTREAM=api:8001 \
    WEB_ROOT=/usr/share/nginx/html \
    WEB_LISTEN=8080 \
    PUBLIC_SCHEME=http \
    TRUSTED_PROXY_CIDR=127.0.0.1/32 \
    NGINX_ENVSUBST_FILTER=API_UPSTREAM|WEB_ROOT|WEB_LISTEN|PUBLIC_SCHEME|TRUSTED_PROXY_CIDR
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1:8080/web-health || exit 1
