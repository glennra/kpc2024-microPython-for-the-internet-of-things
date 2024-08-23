from machine import Pin, Timer, RTC
import time
import micropython

rtc = RTC()
def schedule_func(arg):
    dt = rtc.datetime()
    print("schedule_func()", dt)

led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()
    micropython.schedule(schedule_func, None)

# equivalent: freq=2.5
tim.init(period=400, mode=Timer.PERIODIC, callback=tick)

while True:
    print("Waiting around, spinning", rtc.datetime())
    start = time.ticks_ms()
    a = 0
    while time.ticks_diff(time.ticks_ms(), start) < 2000:
        a += time.ticks_ms() # do something to occupy the CPU
    print("ticks", a)
    
    
    
