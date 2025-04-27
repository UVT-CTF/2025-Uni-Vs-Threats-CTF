FROM ubuntu:23.04
RUN sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    apt update -y && \
    apt install -y xinetd && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt update -y && apt install -y gcc xinetd && apt clean && rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/solver -u 8888 -m solver
USER solver

COPY --chown=solver:solver xinetd /etc/xinetd.d/xinetd
COPY --chown=solver:solver private /home/solver

RUN chmod +x /home/solver/*

CMD ["/usr/sbin/xinetd", "-dontfork"]