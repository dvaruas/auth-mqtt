import paho.mqtt.client as mqtt

import threading

class A:
    def __init__(self):
        self.a = 6

    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
        print(self.a)
        client.disconnect()

    def on_msg(self, client, userdata, message):
        print("Inside on_msg")

a = A()
client = mqtt.Client()
client.connect(host="localhost", port=1883)
client.message_callback_add("a", a.on_message)
client.message_callback_add("a/b", a.on_msg)
#client.on_message = a.on_message
client.subscribe("a/#")
client.loop_forever()
