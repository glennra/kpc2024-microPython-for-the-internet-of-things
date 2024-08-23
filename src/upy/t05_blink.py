# Blink the on-board LED
from machine import Pin
import utime
led = Pin('LED', Pin.OUT)
# led = Pin('EXT_GPIO0', Pin.OUT) # also works
delay = 100
while True:
    led.value(1) # or led.on()
    utime.sleep_ms(delay)
    led.value(0) # or led.off()
    utime.sleep_ms(delay)
