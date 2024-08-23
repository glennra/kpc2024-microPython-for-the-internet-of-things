import socket
import network
import utime
from machine import ADC, Pin
import gc

gc.enable()

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Network name (ssid) and password
ssid = 'rp2-pico'
password = 'kiwipycon'

wlan.connect(ssid, password)

while wlan.status() != network.STAT_GOT_IP:
    print("wlan status:", wlan.status())
    utime.sleep_ms(500)

print(wlan.ifconfig())
wlan.ifconfig(("192.168.2.134", "255.255.255.0", "192.168.2.1", "1.1.1.1"))
print(wlan.ifconfig())

udp_ip = "192.168.2.2"
udp_port = 8001

adc = ADC(ADC.CORE_TEMP)

# can't do this. uPy doesn't support it
# with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
while True:
    try:
        adc_voltage = adc.read_u16() * 3.3 / 65535
        temp_c = round(27 - (adc_voltage - 0.706)/0.001721, 1)

        text = "Hello1234567890"
        text_length = len(text)
        color_rgb = (255, 0, 255)  # Magenta color
        value = int(temp_c * 10)

        v = ((value >> 8) & 0xFF, value & 0xFF)
        message = bytearray([text_length]) + text.encode('utf-8') \
            + bytearray(color_rgb) + bytearray(v)

        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        n = sock.sendto(message, (udp_ip, udp_port))
        #sock.close()
        print("sent", n)
        print("mem", gc.mem_free())
        gc.collect()
        print("mem", gc.mem_free())
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        break
    except Exception as e:
        print(str(e))

utime.sleep_ms(2000)
