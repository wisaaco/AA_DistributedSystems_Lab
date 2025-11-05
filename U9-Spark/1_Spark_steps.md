# Apache Spark installation 

## Containers

```bash
docker network create sparknet
docker run -it --rm --memory 2Gb --cpus 1 -p 9090:4040 -p 7077:7077 -p 8080:8080 --network sparknet --name master ubuntu

docker run -it --rm --memory 2Gb --cpus 1 --network sparknet --name worker1 ubuntu 

docker run -it --rm --memory 2Gb --cpus 1 --network sparknet --name worker2 ubuntu 
(...)

apt update
apt install openjdk-17-jdk nano wget
```

Download Spark:
- https://spark.apache.org/
- https://dlcdn.apache.org/spark/spark-3.5.7/spark-3.5.7-bin-hadoop3.tgz

Steps:
```bash
cd opt
tar -xf spark-3.5.7-bin-hadoop3.tgz
cd spark-3.5.7-bin-hadoop3

# master (log?)
./sbin/start-master.sh -h master

# workers
./sbin/start-worker.sh spark://master:7077




# and from one of those places, we can run: pyspark
./bin/pyspark

Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.5.7
      /_/

Using Python version 3.12.3 (main, Aug 14 2025 17:47:21)
Spark context Web UI available at http://fafcbcb3d0c1:4040
Spark context available as 'sc' (master = local[*], app id = local-1762332289831).
SparkSession available as 'spark'.
>>>


# sc = SparkContext()
lines = sc.textFile("README.md") # Create an RDD called lines
lines.count() 
lines.first() 

# Y respectivamente:
./sbin/stop-worker.sh 
./sbin/stop-master.sh

```

Master's GUI:
- http://localhost:8080/  
- http://localhost:8080/jobs/
    


## Run code from a file

The content:
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

The command:
```bash
./bin/spark-submit --master local SimpleApp.py

./bin/spark-submit --master spark://0.0.0.0:7077 SimpleApp.py

```


## Activities
- Do a docker-compose
- Analyse the Page Rank algorithm: https://cs.brown.edu/courses/cs016/static/files/assignments/projects/GraphHelpSession.pdf

