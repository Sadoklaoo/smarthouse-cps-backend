# app/services/mqtt_client.py

import os
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# Topics for listening and controlling devices
MOTION_SENSOR_TOPIC = "sensor/living_room/motion"
LIGHT_CONTROL_TOPIC = "device/living_room_light/control"

# Track motion detection state
last_motion_time = None
MOTION_TIMEOUT_SECONDS = 10

# Define what happens when connected
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        client.subscribe(MOTION_SENSOR_TOPIC)
        print(f"📡 Subscribed to {MOTION_SENSOR_TOPIC}")
    else:
        print("❌ Failed to connect, return code:", rc)

# Define what happens on receiving a message
def on_message(client, userdata, msg):
    global last_motion_time

    payload = msg.payload.decode()
    topic = msg.topic

    print(f"📥 Received message on {topic}: {payload}")

    if topic == MOTION_SENSOR_TOPIC:
        if payload == "detected":
            last_motion_time = time.time()
            print("💡 Motion detected! Turning ON light.")
            client.publish(LIGHT_CONTROL_TOPIC, "on")

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Main loop
def automation_loop():
    global last_motion_time
    client.loop_start()

    try:
        while True:
            if last_motion_time and (time.time() - last_motion_time > MOTION_TIMEOUT_SECONDS):
                print("⏳ No motion detected. Turning OFF light.")
                client.publish(LIGHT_CONTROL_TOPIC, "off")
                last_motion_time = None
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Stopping automation loop...")
        client.loop_stop()

# Start automation
if __name__ == "__main__":
    automation_loop()
