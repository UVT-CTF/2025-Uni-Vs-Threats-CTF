# Use a minimal Go image
FROM golang:1.24 as builder

# Set build env
WORKDIR /build

# Copy source code
COPY . .

# Build the Go server
RUN go mod init ctfserver && go mod tidy && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o server main.go

# -----------------
# Final minimal container
FROM debian:bullseye-slim

# Install minimal required packages (e.g., ca-certificates if needed)
RUN apt-get update && apt-get install -y ca-certificates && apt-get clean

# Copy built server and public folder
COPY --from=builder /build/server /server
COPY --from=builder /build/public /public
COPY --from=builder /build/secret /secret
COPY entrypoint.sh /entrypoint.sh

# Give permissions
RUN chmod +x /entrypoint.sh

# Expose the port
EXPOSE 40048

# Start the server through entrypoint
ENTRYPOINT ["/entrypoint.sh"]
