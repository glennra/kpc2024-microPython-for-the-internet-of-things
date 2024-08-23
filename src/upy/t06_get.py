import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
from time import sleep_ms

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = 'rp2-pico'
password = 'kiwipycon'

wlan.connect(ssid, password)

while not wlan.status() in [network.STAT_GOT_IP]:
    print("wlan status:", wlan.status())
    sleep_ms(500)
    
print(wlan.ifconfig()) # IP from DHCP 
wlan.ifconfig(("192.168.2.155", "255.255.255.0", "192.168.2.1", "1.1.1.1"))
print(wlan.ifconfig())

#print(wlan.config("mac").hex())
#print(wlan.config("txpower"))

url_list = ["http://ip.jsontest.com/", "http://date.jsontest.com/"]

for url in url_list:

    print('about to get', url)

    # Get the data from the server
    response = urequests.get(url)

    # Print the server's response
    print(response.text)
