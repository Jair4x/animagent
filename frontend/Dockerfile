FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json bun.lockb ./
RUN npm install -g bun && bun install

COPY . .

ARG PUBLIC_API_URL=http://localhost:8000
ENV PUBLIC_API_URL=$PUBLIC_API_URL

RUN bun run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
