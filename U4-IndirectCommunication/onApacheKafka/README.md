# Run a Kafka cluster with 3 brokers

docker-compose up -d

# Creating topics

docker exec onapachekafka-kafka1-1 kafka-topics --create --topic group-counter --partitions 3 --replication-factor 3 --bootstrap-server localhost:9092

# Python 
 - Dependencies:
   - confluent-kafka