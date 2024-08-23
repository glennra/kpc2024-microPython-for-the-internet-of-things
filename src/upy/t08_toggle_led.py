from rp2 import bootsel_button
from machine import Pin
import time

led =  Pin('LED', Pin.OUT)
oldstate = False
while True:
    newstate = bootsel_button()
    if newstate ==  True and oldstate == False:
        led.toggle()
    oldstate = newstate
    #time.sleep_ms(50)
