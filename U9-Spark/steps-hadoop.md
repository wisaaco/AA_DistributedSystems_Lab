
# Actividad HDFS 

Imagen del cluster de hadoop:
https://github.com/big-data-europe/docker-hadoop

Una vez funcionando
```bash
docker exec -it namenode /bin/bash
```

Algunos comandos de HDFS:
```bash
# HDFS list commands to show all the directories in root "/"
hdfs dfs -ls /
# Create a new directory inside HDFS using mkdir tag.
hdfs dfs -mkdir -p /user/root
# Copy the files to the input path in HDFS.
hdfs dfs -put <file_name> <path>
# Have a look at the content of your input file.
hdfs dfs -cat <input_file>
```

## Ejecución de MapReduce

```bash
docker exec -it datanode /bin/bash
find / -name *mapreduce*
yarn jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar pi 10 10
```
hdfs://namenode:9000/hola.txt


#### Varios

```bash
docker cp <file_name> namenode:/<path>
http://<your_ip_address>:9870
ssh -L 9870:localhost:9870 Isaac@…
```
