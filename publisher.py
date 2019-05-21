import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("192.168.1.2")

while True:
    client.publish("syssmtcars",input())