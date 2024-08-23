import gc
from machine import Pin, ADC
import micropython
import utime
import socket

gc.threshold((gc.mem_free() + gc.mem_alloc()) // 4)

print("mem", gc.mem_free())
gc.collect()
print("mem", gc.mem_free())

import wifi
wifi.connect()

print("mem", gc.mem_free())
gc.collect()
print("mem", gc.mem_free())

udp_ip = "192.168.2.2"
udp_port = 8001

# save state
last_col = '' 

def set_colour(arg):
    global last_col
    if arg != last_col:
        print(arg)
        last_col = arg
        text = "Glenn "
        text_length = len(text)
        r = g = b = 0
        if arg == 'red':
            r = 0xFF
        elif arg == 'orange':
            r = 0xFF
            g = 0x7E
        elif arg == 'green':
            g = 0xFF
        color_rgb = (r, g, b)

        value = 0

        v = ((value >> 8) & 0xFF, value & 0xFF)
        message = bytearray([text_length]) + text.encode('utf-8') \
            + bytearray(color_rgb) + bytearray(v)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        n = sock.sendto(message, (udp_ip, udp_port))
        print("mem", gc.mem_free())
        sock.close()
        print("mem", gc.mem_free())
        #gc.collect()


# Set up ADC to read voltage from microphone
adc = ADC(0)

sound_max = 2**16
sound_red = 2**13
sound_yel = 2**12
sound = 0

forget = 100
sample_period = 50 # ms
count = 0
while True:
    start = utime.ticks_ms()
    mx = 0
    mn = 2**16
    while utime.ticks_diff(utime.ticks_ms(), start) < sample_period:
        val = adc.read_u16()
        count += 1
        if val > mx:
            mx = val
        if val < mn:
            mn = val

    peak_to_peak = mx - mn

    #print(peak_to_peak)
    if peak_to_peak > sound:
        sound = peak_to_peak

    if sound > sound_max:
        sound = sound_max

    if sound > sound_red:
        micropython.schedule(set_colour, "red")
    elif sound > sound_yel:
        micropython.schedule(set_colour, "orange")
    else:
        micropython.schedule(set_colour, "green")

    #print(count, sound)
    count = 0

    sound -= forget
    if sound < 0:
        sound = 0

