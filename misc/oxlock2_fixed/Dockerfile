FROM python:3.10-slim-buster

ENV TERM xterm-256color

# Install process tools, network tools and debugging utilities
RUN apt update && apt install -y \
    xinetd \
    procps \
    net-tools \
    curl \
    netcat \
    telnet \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install colorama

# Create user structure
RUN useradd -d /home/player -u 8999 -m player && \
    mkdir -p /home/player/private && \
    chown player:player /home/player/private

# Copy files (note: this will fail as non-root user)
COPY xinetd /etc/xinetd.d/0xLOcK
COPY private /home/player/private
RUN chown player:player /etc/xinetd.d/0xLOcK && \
    chown -R player:player /home/player/private

# Set permissions
RUN chmod 750 /home/player/private/0xL0cK.py && \
    chmod 644 /etc/xinetd.d/0xLOcK

# Expose the service port
EXPOSE 8654

# Start xinetd service
CMD ["/usr/sbin/xinetd", "-dontfork", "-stayalive", "-filelog", "/dev/stdout"]