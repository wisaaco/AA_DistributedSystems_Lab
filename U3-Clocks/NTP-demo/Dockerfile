FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends chrony tzdata iproute2 \
    && mkdir -p /var/lib/chrony /var/log/chrony /run/chrony \
    && chown _chrony:_chrony /var/lib/chrony /var/log/chrony /run/chrony \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
