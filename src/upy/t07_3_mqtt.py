from umqtt.simple import MQTTClient
import network
import utime
from machine import Pin
from machine import ADC

led = Pin("LED", Pin.OUT)
# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Network name (ssid) and password
ssid = 'rp2-pico'
password = 'kiwipycon'

wlan.ifconfig(("192.168.2.155", "255.255.255.0", "192.168.2.1", "1.1.1.1"))

wlan.connect(ssid, password)

while wlan.status() != network.STAT_GOT_IP:
    print("wlan status:", wlan.status())
    utime.sleep_ms(500)
    led.toggle()

print(wlan.ifconfig())

# Define MQTT parameters
broker_address = "192.168.2.2"  # Our broker's IP address
client_id = "mqtt_client"
topic = b"grid/55"

adc = ADC(4)
client = MQTTClient(client_id, broker_address)

while True:
    try:
        adc_voltage = adc.read_u16() * 3.3 / 65535
        temp_c = round(27 - (adc_voltage - 0.706)/0.001721, 1)

        text = "Glenn "
        text_length = len(text)
        color_rgb = (0, 255, 0)  # Green color

        value = int(temp_c * 10)
        print("value", value, "topic", topic)
        v = ((value >> 8) & 0xFF, value & 0xFF) # 16 bit / 2 byte unsigned integer
        message = bytearray([text_length]) + text.encode('utf-8')\
             + bytearray(color_rgb) + bytearray(v)

        client.connect()
        client.publish(topic, message)
        client.disconnect()
        
        utime.sleep_ms(2000)

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        break
    except Exception as e:
        print(str(e))

