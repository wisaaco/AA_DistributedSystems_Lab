# NTP demo with Docker + chrony

NTP **can serve and query time inside containers**. What it cannot do is give each container its own wall clock: Linux containers share `CLOCK_REALTIME` with the Docker host/VM. On Docker Desktop for Mac that clock belongs to the Linux VM, not to each container.

That is why a naive `chronyd` often dies with:

```text
Fatal error : adjtimex(...) failed : Operation not permitted
```

This compose file works around that:

- `chronyd -x` does not try to step the kernel clock
- `seccomp:unconfined` allows the read-only `clock_adjtime` probe at startup
- timezone is only a **display** offset (`TZ`), not a different UTC clock

To actually set a wrong date on the master and watch a client jump (the 1980 experiment), use the Multipass VMs in `../A_ConfiguringLocalNTPServer.md`. Each VM has its own kernel clock.

## Run

Start Docker Desktop first, then:

```bash
cd U3-Clocks/NTP-demo
docker compose up --build
```

Wait until both containers print `chronyd ... started`. In another terminal:

```bash
# Local time differs because of TZ (Tokyo vs Madrid)
docker exec ntp-master date
docker exec ntp-client date

# UTC is the same: one shared kernel clock
docker exec ntp-master date -u
docker exec ntp-client date -u

# NTP protocol: client should show ntp-master as a reachable source (*)
docker exec ntp-client chronyc sources -v
docker exec ntp-client chronyc tracking
docker exec ntp-client chronyc sourcestats -v
```

`chronyc tracking` reports the measured offset. With `-x` that offset is **not** applied to the OS clock (by design).

Do **not** run `date --set=...` or `chronyd -q` here. It either fails with `Operation not permitted`, or it changes the Docker VM clock and breaks TLS/image pulls.

```bash
docker compose down
```
