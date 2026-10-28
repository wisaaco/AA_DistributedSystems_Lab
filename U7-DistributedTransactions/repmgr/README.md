

# Pasos

0. Leer `docker-compose.yml`

1. Vemos como está montado el clúster:

```bash
#### Si segunda vez....
docker compose down -v 

docker compose up -d

docker exec -it pg-0 repmgr -f /opt/bitnami/repmgr/conf/repmgr.conf cluster show
```

2. Hard o Soft state?

Escribimos en el primario:

```bash
docker exec -it pg-0 psql -U myuser -d mydb -c "CREATE TABLE test (id SERIAL, data TEXT); INSERT INTO test (data) VALUES ('Hola mundo desde el primario');"
```

Leemos en el secundario:

```bash
docker exec -it pg-1 psql -U myuser -d mydb -c "SELECT * FROM test;"
```

Escribimos en el secundario (!):
```bash
docker exec -it pg-1 psql -U myuser -d mydb -c "INSERT INTO test (data) VALUES ('Intento fallido');"
```

3. Fallo 

```bash
docker stop pg-0

docker exec -it pg-1 repmgr -f /opt/bitnami/repmgr/conf/repmgr.conf cluster show

docker exec -it pg-1 psql -U myuser -d mydb -c "INSERT INTO test (data) VALUES ('Mi primario caido :( )');"
docker exec -it pg-1 psql -U myuser -d mydb -c "SELECT * FROM test;"
```

Wait a daemon... si necesario promovemos el standby(1) a nuevo primario 
```bash
docker exec -it pg-1 repmgr -f /opt/bitnami/repmgr/conf/repmgr.conf standby promote
```

4. Recuperamos el pg-0

- ¿Qué pasará?

```bash
Actividad
```
