import paho.mqtt.publish as publish


#client = mqtt.Client()
#client.connect(host="localhost", port=1883)
publish.single("house/light","ON")
publish.single("a/b", "p")
publish.single("a", "p")
