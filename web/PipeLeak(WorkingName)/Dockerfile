
FROM node:alpine

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Install system dependencies
RUN apk add --no-cache \
    supervisor \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    apache2-utils

# Create working directory
WORKDIR /app

# Preinstall dependencies (copy only package.json files for cache efficiency)
COPY ./private/challenge/package*.json ./
RUN npm install

# Copy flag securely into the container
COPY ./private/flag.txt /

EXPOSE 8080

CMD ["sh", "-c", "npm install && node index.js"]
