import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
from time import sleep_ms

from machine import Pin

led = Pin("LED", Pin.OUT)

def connect():
    # Init network object
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Some info
    print("mac", wlan.config("mac").hex())
    print("tx power", wlan.config("txpower"))

    # Wifi scan
    wifi_list = wlan.scan()
    print(wifi_list)

    # Fill in your network name (ssid) and password here:
    ssid = 'rp2-pico'
    password = 'kiwipycon'

    wlan.connect(ssid, password)

    # Note that if there is no DHCP server then after successful
    # connection wlan.status() will be 2 (CYW43_LINK_NOIP) which
    # is not defined by the MicroPython network module.
    # In this case call wlan.ifconfig([...]) prior to wlan.connect().

    # Can also use wlan.isconnected() here
    while not wlan.status() in [network.STAT_GOT_IP]:
        print("wlan status:", wlan.status())
        led.toggle()
        sleep_ms(500)
    print("IP from DHCP", wlan.ifconfig()) # IP from DHCP 

    # Set static IP
    wlan.ifconfig(("192.168.2.155", "255.255.255.0", "192.168.2.1", "1.1.1.1"))
    print("Static IP", wlan.ifconfig())

    # uPy for the Pico doesn't have this yet 
    # wlan.config(dhcp_hostname = "glenn")

def create_ap():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid="ssid", password="password")
    ap.active(True)
    while ap.active() == False:
        pass
    print("AP active")
    print(ap.ifconfig())


def get():
    url_list = ["http://ip.jsontest.com/", "http://date.jsontest.com/"]

    for url in url_list:

        print('about to get', url)

        # Get the data from the server
        response = urequests.get(url)

        # Print the server's response
        print(response.text)
