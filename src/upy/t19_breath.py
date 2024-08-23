from machine import Pin
#from machine import Timer
from machine import PWM
from time import sleep

# Connect the power lead of the KY-038 to PIN 21. This allows the board
# to be powered by the PWM and the onboard LED will be dimmed.

led = Pin("GPIO16", Pin.OUT)
pwm = PWM(led)
duty_step = 129  # Step size for changing the duty cycle

freq = 5000
pwm.freq(freq)

try:
    while True:
      # Increase the duty cycle gradually
      for duty_cycle in range(8*duty_step, 65536, duty_step):
        pwm.duty_u16(duty_cycle)
        sleep(0.005)
        
      # Decrease the duty cycle gradually
      for duty_cycle in range(65536, 8*duty_step, -duty_step):
        pwm.duty_u16(duty_cycle)
        sleep(0.005)
    
      sleep(1.5)
        
except KeyboardInterrupt:
    print("Keyboard interrupt")
    pwm.duty_u16(0)
    print(pwm)
    pwm.deinit()
