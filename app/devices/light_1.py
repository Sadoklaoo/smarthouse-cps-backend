import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("💡 light_1 connected to MQTT Broker")
        client.subscribe("device/light_1/control")
    else:
        print("❌ light_1 failed to connect, return code", rc)

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    if command == "on":
        print("💡 light_1 turned ON")
    elif command == "off":
        print("💤 light_1 turned OFF")
    else:
        print(f"⚠️ Unknown command for light_1: {command}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt", 1883, 60)
client.loop_forever()
