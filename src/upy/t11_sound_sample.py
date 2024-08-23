from machine import Pin, ADC
import utime

# Set up ADC to read voltage from sound sensor
adc = ADC(0) # or ADC(Pin(26))

while True:
    sample = adc.read_u16()
    print(sample)
