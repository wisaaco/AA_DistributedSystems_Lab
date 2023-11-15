# Pasos de instalación de HBASE en modo standalone

Fuente y pasos:
https://hbase.apache.org/book.html#quickstart

Preparación de container
```bash
docker run -it --rm --memory 2Gb --cpus 1 -p 9090:9090 -p 16010:16010 --network sparknet --name hbase-master ubuntu
apt update
apt install openjdk-17-jdk wget nano
cd opt
wget https://dlcdn.apache.org/hbase/2.5.6/hbase-2.5.6-bin.tar.gz
tar -xf hbase-2.5.6-bin.tar.gz 
cd hbase-2.5.6
```

Configuración de Java:
```bash
update-alternatives --list java
>>> /usr/lib/jvm/java-17-openjdk-arm64/bin/java

nano conf/hbase-env.sh
# Set environment variables here.
# The java implementation to use.
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64 
cd ../bin
```

Lanzamiento de hbase
```bash
./start-hbase.sh
```

Ahora ya funciona la web:
http://localhost:16010 


## Hbase shell

```bash
./hbase shell
```

Algunos comandos:

```bash 
status
create 'emp', 'personal data', 'professional data'
put 'emp','1','personal data:name','Fulanito'
put 'emp','1','personal data:city','Palma'
put 'emp','1','professional data:designation','maanger' 
put 'emp','1','professional data:salary','50000'
scan 'emp'
get 'emp', '1'
get 'emp', '1', {COLUMN => 'personal data:name'}
```



## Python connection

Para conectarse a Python necesitamos thrift service

```bash
nohup ./hbase thrift start &
```

Y finalmente:
```python
# https://happybase.readthedocs.io/en/latest/
# https://happybase.readthedocs.io/en/latest/user.html

import happybase

connection = happybase.Connection('localhost', 9090)
connection.tables()
```


## Importing TSV/CSV files
  
  ``````
  id    c1  c2


row1    1   22
row2    e1  42
``````

Con o sin separador TSV v CSV:
```
./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=, -Dimporttsv.columns=HBASE_ROW_KEY,cf:c1,cf:c2 mytable5 testTSV.tsv
```