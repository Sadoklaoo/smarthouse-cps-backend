import paho.mqtt.publish as publish

publish.single(
    topic="device/light_1/control",
    payload="on",
    hostname="mqtt",  # this matches your Docker service name
    port=1883
)

print("📤 Sent 'on' command to light_1")
