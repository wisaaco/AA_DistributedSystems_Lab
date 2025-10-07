import paho.mqtt.client as mqtt
import time
import json
import paho.mqtt.client as mqttClient

# MQTT Broker settings
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "demo/sensor/data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Publisher connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")

def main():
    # Create MQTT client
    client = mqtt.Client(client_id="PublisherDemo", callback_api_version=mqttClient.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        # Connect to broker
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        client.loop_start()
        
        # Publish messages
        message_count = 0
        while message_count < 10:
            # Create sample sensor data
            sensor_data = {
                "sensor_id": "sensor_001",
                "temperature": 20 + message_count * 0.5,
                "humidity": 50 + message_count * 2,
                "timestamp": time.time(),
                "message_id": message_count
            }
            
            # Convert to JSON and publish
            payload = json.dumps(sensor_data)
            result = client.publish(TOPIC, payload, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Published: {payload}")
            else:
                print(f"Failed to publish message {message_count}")
            
            message_count += 1
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("Publisher stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Publisher disconnected")

if __name__ == "__main__":
    main()