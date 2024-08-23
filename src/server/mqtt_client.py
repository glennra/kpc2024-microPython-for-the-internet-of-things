import paho.mqtt.client as mqtt

broker_address = "192.168.2.2"
port = 1883
topic = "grid/47"

text = "Hello"
text_length = len(text)
color_rgb = (0, 255, 0)  # Green color

value = 12345
v = ((value >> 8) & 0xFF, value & 0xFF) # 16 bit/ 2 byte unsigned integer
message = bytearray([text_length]) + text.encode('utf-8')\
     + bytearray(color_rgb) + bytearray(v)

client = mqtt.Client()
client.connect(broker_address, port, 60)
client.publish(topic, message)
client.disconnect()
