import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# When connected to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        # Subscribe to device control topic
        client.subscribe("device/light_1/control")
    else:
        print("❌ Failed to connect, return code", rc)

# When a message is received
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    print(f"📥 Message received on {topic}: {payload}")

    # Handle device logic
    if topic == "device/light_1/control":
        if payload == "on":
            print("💡 Turning ON light_1")
        elif payload == "off":
            print("💡 Turning OFF light_1")

# Create MQTT client and attach callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker and start listening
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
