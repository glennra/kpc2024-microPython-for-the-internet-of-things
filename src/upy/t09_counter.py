import micropython
from rp2 import bootsel_button
import time
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import gc

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = 'rp2-pico'
password = 'kiwipycon'

wlan.connect(ssid, password)

while not wlan.status() in [network.STAT_GOT_IP]:
    print("wlan status:", wlan.status())
    time.sleep_ms(500)
    
print(wlan.ifconfig()) # IP from DHCP 
wlan.ifconfig(("192.168.2.155", "255.255.255.0", "192.168.2.1", "1.1.1.1"))
print(wlan.ifconfig())

last_col = ""
url = "http://192.168.2.2:8000"

def set_colour(arg):
    global last_col
    if arg != last_col:
        print(arg)
        last_col = arg

        data = {
            'text': "Glenn",
            'color': arg
            }

        print('about to post to', url, 'with data', data)
        # Post the data to the server
        response = urequests.post(url, json=data)
    gc.collect()

count = 0
while True:
    if bootsel_button():
        count += 1
    else:
        count -= 1
        if count < 0:
            count = 0

    if count >= 40:
        micropython.schedule(set_colour, 'red')
    elif count >= 20:
        micropython.schedule(set_colour, 'orange')
    else:
        micropython.schedule(set_colour, 'green')

    time.sleep_ms(50)

