#!/bin/bash
set -euo pipefail

mkdir -p /var/lib/chrony /var/log/chrony /run/chrony
chown _chrony:_chrony /var/lib/chrony /var/log/chrony /run/chrony
chmod 750 /var/lib/chrony /var/log/chrony /run/chrony

# -d: stay in foreground (required for Docker)
# -x: do not discipline CLOCK_REALTIME (containers share the host/VM clock)
# -F 0: disable chrony's own seccomp filter, which conflicts with Docker's
exec chronyd -d -x -F 0 -f /etc/chrony/chrony.conf
