# frontend/Dockerfile

FROM node:20-alpine as build

WORKDIR /app
COPY . .

RUN npm install
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist/autodidact-frontend/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

