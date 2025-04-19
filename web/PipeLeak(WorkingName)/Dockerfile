FROM node:alpine

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
RUN apk add --no-cache \
    supervisor \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    apache2-utils

RUN mkdir -p /app 
COPY ./private/challenge /app

WORKDIR /app
RUN npm i

COPY ./private/flag.txt /

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

EXPOSE 8080

CMD ["node", "index.js"]
