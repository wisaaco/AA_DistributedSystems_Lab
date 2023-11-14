# Pasos de instalación de Spark 

## Configuración de containers

```bash
docker run -it --rm --memory 2Gb --cpus 1 -p 9090:4040 -p 7077:7077 -p 8080:8080 --network sparknet --name master ubuntu

docker run -it --rm --memory 2Gb --cpus 1 --network sparknet --name worker1 ubuntu 

docker run -it --rm --memory 2Gb --cpus 1 --network sparknet --name worker2 ubuntu 
(...)

apt update
apt install openjdk-17-jdk nano wget
```

Descarga de imagen
```bash
cd opt
tar -xf spark-3.5.0-bin-hadoop3.tgz
cd spark-3.5.0-bin-hadoop3


./sbin/start-master.sh -h 0.0.0.0
./sbin/start-worker.sh spark://172.22.0.2:7077
./sbin/start-worker.sh spark://172.22.0.2:7077 ##

./sbin/stop-worker.sh 
./sbin/stop-master.sh

# Desde aquí
./bin/pyspark

#sc = SparkContext()
lines = sc.textFile("README.md") # Create an RDD called lines
lines.count() 
lines.first() 
```

Y: http://localhost:8080/jobs/


## Run code 

```python
from pyspark.sql import SparkSession

logFile = "README.md"  # Should be some file on your system
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text(logFile).cache()

numAs = logData.filter(logData.value.contains('a')).count()
numBs = logData.filter(logData.value.contains('b')).count()

print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

spark.stop()
```

Desde
```bash
./bin/spark-submit --master local SimpleApp.py
```



## Activity 
Page Rank
https://cs.brown.edu/courses/cs016/static/files/assignments/projects/GraphHelpSession.pdf


### Varios
docker start 
docker attach
/opt/spark-3.5.0-bin-hadoop3/logs/spark--org.apache.spark.deploy.master.Master-1-localhost.out


### Testing code

Desde pyspark:
