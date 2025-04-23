FROM node:alpine

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

RUN apk add --no-cache \
    supervisor \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    apache2-utils

WORKDIR /app

COPY ./challenge ./
RUN npm install

EXPOSE 8080

CMD ["sh", "-c", "npm install && node index.js"]
