from machine import Pin, ADC
import utime

# Set up ADC to read voltage from microphone
#adc = ADC(Pin(26))
adc = ADC(0)

sound = 0

sound_max = 2**16
sound_red = 2**13
sound_yel = 2**12

forget = 200
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
        print("red")
    elif sound > sound_yel:
        print("yellow")
    else:
        print("green")

    print(count, sound)
    count = 0

    sound -= forget
    if sound < 0:
        sound = 0

