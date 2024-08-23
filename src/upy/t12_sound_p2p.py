from machine import Pin, ADC
import utime

# Set up ADC to read voltage from sound sensor
adc = ADC(0) # or ADC(Pin(26))

while True:
    start = utime.ticks_ms()
    sample_max = 0 # minimum possible sample value
    sample_min = 2**16 # maximum possible sample value
    while utime.ticks_diff(utime.ticks_ms(), start) < 100:
        sample = adc.read_u16()
        if sample > sample_max:
            sample_max = sample
        elif sample < sample_min:
            sample_min = sample 
    level = sample_max - sample_min
    print(level)

