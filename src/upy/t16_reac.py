"""
Wait for a button press.

Flash the LED to indicate we are about to start.

Wait a random time.

Turn the LED on.

Measure the time until the button is pressed.

Report the result to the leaderboard.

Game the leaderboard.

"""

from machine import Pin
import utime
import urandom
from rp2 import bootsel_button
import network   # handles connecting to WiFi

# Setup LED
led = Pin("LED", Pin.OUT)

led.off()

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

        led.off()
        # Flash the LED
        for i in range(3):
            led.toggle()
            utime.sleep_ms(100)
#             led.value(1)
#             utime.sleep_ms(100)

        led.value(0)

        # Wait for a random time between 2 and 5 seconds
        delay = urandom.uniform(2, 5)
        utime.sleep(delay)

        # Turn on LED
        led.value(1)
        
        # Record the time when the LED is turned on
        start_time = utime.ticks_us()

        # Wait for button press
        press_time = wait_for_button_press()

        # Calculate reaction time in milliseconds
        reaction_time = (press_time - start_time) / 1000

        # Turn off LED
        led.value(0)

        # Print reaction time
        print("Reaction time: {:.2f} ms".format(reaction_time))

        # Wait before the next round
        utime.sleep(2)

# Run the game
main()