ETCD
====
- https://en.wikipedia.org/wiki/Etcd
- https://etcd.io/
- https://hub.docker.com/r/bitnami/etcd


docker run -d --name etcd-server \
  -p 2379:2379 -p 2380:2380 \
  -e ALLOW_NONE_AUTHENTICATION=yes \
  -e ETCD_ADVERTISE_CLIENT_URLS=http://0.0.0.0:2379 \
  bitnami/etcd:latest

docker exec -it etcd-server etcdctl \
  --endpoints=http://127.0.0.1:2379 put mundo "holis"

docker exec -it etcd-server etcdctl \
  --endpoints=http://127.0.0.1:2379 get mundo 


docker exec -it etcd-server etcdctl \
  --endpoints=http://127.0.0.1:2379 watch mundo