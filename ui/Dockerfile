# Build stage
FROM node:18-alpine AS build-stage

ARG VITE_FRONTEND_SERVICE_URL
ARG VITE_GOOGLE_OAUTH_CLIENT_ID
ARG VITE_GOOGLE_OAUTH_REDIRECT_URL

ENV FRONTEND_SERVICE_URL=$VITE_FRONTEND_SERVICE_URL
ENV VITE_GOOGLE_OAUTH_CLIENT_ID=$VITE_GOOGLE_OAUTH_CLIENT_ID
ENV VITE_GOOGLE_OAUTH_REDIRECT_URL=$VITE_GOOGLE_OAUTH_REDIRECT_URL

ENV NODE_ENV="production"

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

# Production stage
FROM nginx:stable-alpine AS production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
