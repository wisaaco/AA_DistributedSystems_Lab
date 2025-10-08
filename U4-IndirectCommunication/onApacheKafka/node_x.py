from confluent_kafka import Producer, Consumer, KafkaException
import threading
import time
import json

BOOTSTRAP_SERVERS = 'localhost:9092,localhost:9093,localhost:9094'
TOPIC = 'group-counter'

def node(node_id):
    producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

    consumer = Consumer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': f'group_{node_id}',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([TOPIC])

    counter = 0

    def send_update():
        producer.produce(TOPIC, json.dumps({'node': node_id, 'delta': 1}).encode())
        producer.flush()

    # Start by sending an update periodically
    def generate_updates():
        while True:
            send_update()
            time.sleep(3 + node_id)  # different pace per node

    threading.Thread(target=generate_updates, daemon=True).start()

    print(f"Node {node_id} started.")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        data = json.loads(msg.value().decode())
        counter += data['delta']
        print(f"Node {node_id} sees counter = {counter} after update from {data['node']}")
