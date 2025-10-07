import paho.mqtt.client as mqtt
import json
import paho.mqtt.client as mqttClient

# MQTT Broker settings
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "demo/sensor/data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Subscriber connected to MQTT Broker!")
        # Subscribe to topic
        client.subscribe(TOPIC, qos=1)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        # Parse JSON message
        payload = json.loads(msg.payload.decode())
        print(f"Received message:")
        print(f"  Topic: {msg.topic}")
        print(f"  QoS: {msg.qos}")
        print(f"  Data: {payload}")
        print("-" * 50)
    except json.JSONDecodeError:
        print(f"Received non-JSON message: {msg.payload.decode()}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscription confirmed for message ID: {mid}")

def main():
    # Create MQTT client
    client = mqtt.Client(client_id="SubscriberDemo", callback_api_version=mqttClient.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    
    try:
        # Connect to broker
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        print("Subscriber started. Waiting for messages...")
        print("Press Ctrl+C to stop")
        
        # Start network loop (blocks until disconnected)
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("Subscriber stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
        print("Subscriber disconnected")

if __name__ == "__main__":
    main()