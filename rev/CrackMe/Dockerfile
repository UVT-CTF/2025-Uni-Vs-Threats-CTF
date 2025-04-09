FROM node:20-alpine

# Install http-server globally
RUN npm install -g http-server

# Create app directory
WORKDIR /app

# Copy files
COPY /private/output .

# Run the generation script and start the server
CMD http-server . -p 8080