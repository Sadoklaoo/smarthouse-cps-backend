import time
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# Topics
MOTION_SENSOR_TOPIC = "sensor/living_room/motion"

# Connect to MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("✅ Connected to MQTT Broker.")

# Simulate motion detected
motion_payload = "detected"
print(f"📤 Publishing to topic '{MOTION_SENSOR_TOPIC}' with payload '{motion_payload}'")
client.publish(MOTION_SENSOR_TOPIC, motion_payload)

# Wait for automation to react (e.g. mqtt_client.py should turn on the light)
time.sleep(5)

print("✅ Motion simulation finished.")
client.disconnect()
