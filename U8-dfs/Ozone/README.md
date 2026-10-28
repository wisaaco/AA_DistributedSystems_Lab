# Steps


```bash
docker compose up -d

docker compose up -d --scale datanode=3
```

Webs:

- Ozone Recon [http://localhost:9888/#/Overview](http://localhost:9888/#/Overview)
- Ozone Manager (OM) UI: [http://localhost:9874/#!/](http://localhost:9874/#!/)
- Storage Container Manager (SCM) UI: [http://localhost:9876/#!/](http://localhost:9876/#!/)


```bash
docker compose exec om bash
```

Volumnes:

```bash
ozone sh volume create /vol1
ozone sh bucket create /vol1/bucket1
```

Manejo estilo hdfs:

```bash
hdfs dfs -mkdir -p ofs://om/vol1/bucket1/micarpeta/datos

hdfs dfs -put /etc/hosts ofs://om/vol1/bucket1/micarpeta/datos/

hdfs dfs -ls ofs://om/vol1/bucket1/micarpeta/
```

Manejo estilo Ozone:

```bash
ozone sh volume list /
ozone sh bucket list /vol1
ozone sh key list /vol1/bucket1

docker compose cp mifichero.txt om:/tmp/mifichero.txt
ozone sh key put /vol1/bucket1/file.txt /tmp/mifichero.txt

ozone sh key cat /vol1/bucket1/file.txt

ozone sh key get /vol1/bucket1/file.txt /tmp/file.txt

ozone sh key list /vol1/bucket1

```



