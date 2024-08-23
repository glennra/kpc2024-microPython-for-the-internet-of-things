from rp2 import bootsel_button
from machine import Pin, Timer
import time
import micropython

initial_period = 500
period = initial_period
period_decrement = 200

led = Pin("LED", Pin.OUT)
def tick(timer):
    global led
    led.toggle()

tim = Timer()
tim.init(period=period, mode=Timer.PERIODIC, callback=tick)

def next_freq(the_timer):
    global period
    period -= period_decrement
    if period <= 0:
        period = initial_period
    the_timer.init(period=period, mode=Timer.PERIODIC, callback=tick)

# code pattern from task 8
while True:
    newstate = bootsel_button()
    if newstate ==  True and oldstate == False:
        micropython.schedule(next_freq, tim)
    oldstate = newstate
