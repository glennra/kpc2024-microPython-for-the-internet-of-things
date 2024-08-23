import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import utime
from machine import ADC

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

# Replace DHCP address with a static one
wlan.ifconfig(("192.168.2.151", "255.255.255.0", "192.168.2.1", "1.1.1.1"))

# Define the server URL and the integer value to post
url = 'http://192.168.2.2:8000'

adc = ADC(ADC.CORE_TEMP) # ADC.CORE_TEMP == 4

while True:
    try:
        adc_voltage = adc.read_u16() * 3.3 / 65535
        temp_c = round(27 - (adc_voltage - 0.706)/0.001721, 1)

        data = {
            'text': str(temp_c)+" your name <id>",
            'color': 'cyan' #'#FFFF00'
            }

        print('about to post to', url, 'with data', data)
        # Post the data to the server
        response = urequests.post(url, json=data)

        # Print the server's response
        print("response", response.text)

        utime.sleep_ms(2000)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        break

