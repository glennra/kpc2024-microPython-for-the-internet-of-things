"""
Wait for a button press.

Flash the LED to indicate we are about to start.

Wait a random time.

Turn the LED on.

Measure the time until the button is pressed.

Report the result to the leaderboard.

"""

from machine import Pin
import utime
import urandom
from rp2 import bootsel_button
import network   # handles connecting to WiFi
from umqtt.simple import MQTTClient
import json
import gc

# URL for result
url = 'http://192.168.2.2:8000'

# Setup LED
led = Pin("LED", Pin.OUT)

led.on()

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Fill in your network name (ssid) and password here:
ssid = 'rp2-pico'
password = 'kiwipycon'
wlan.connect(ssid, password)

while wlan.status() != network.STAT_GOT_IP:
    print("wlan status:", wlan.status())
    utime.sleep_ms(500)
    led.toggle()
print(wlan.ifconfig())
wlan.ifconfig(("192.168.2.155", "255.255.255.0", "192.168.2.1", "1.1.1.1"))
print(wlan.ifconfig())

# Define MQTT parameters
broker_address = "192.168.2.2"
client_id = "mqtt_client"
topic = b"reaction"

client = MQTTClient(client_id, broker_address)

led.off()

# # Setup button
# button = Pin(14, Pin.IN, Pin.PULL_DOWN)

def wait_for_button_press():
    while bootsel_button() == 0:
        #utime.sleep_ms(1)
        pass
    return utime.ticks_us()

def main():
    while True:
        # Wait for button press to start
        while bootsel_button() == 0:
            utime.sleep_ms(50)

        # Flash the LED
        led.on()
        for i in range(4):
            utime.sleep_ms(100)
            led.toggle()
        utime.sleep_ms(100)
        led.off()

        # Wait for a random time between 2 to 4 seconds
        delay = urandom.uniform(2, 4)
        utime.sleep(delay)

        # check for cheating
        if bootsel_button():
            continue
        
        # Turn on LED
        led.on()
        
        # Record the time when the LED is turned on
        start_time = utime.ticks_us()

        # Wait for button press
        press_time = wait_for_button_press()

        # Calculate reaction time in milliseconds
        reaction_time = (press_time - start_time) / 1000

        # Turn off LED
        led.off()

        # publish reaction time
        data = {
            'name': 'Glenn' # +str(int(reaction_time)),
            'score': reaction_time
            }
        print(data)
        
        client.connect()
        client.publish(topic, json.dumps(data))
        client.disconnect()
        
        gc.collect()

        # Wait before the next round
        utime.sleep(1)

# Run the game
main()