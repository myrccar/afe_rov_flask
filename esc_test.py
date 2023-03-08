"""
a script to test the esc/motors on the rov pi
"""

import RPi.GPIO as GPIO
import time 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)             # choose BCM or ---BOARD(one we use)---  
GPIO.setup(12, GPIO.OUT)           # set GPIO12 as an output   

try:
    p = GPIO.PWM(12, 50)
    p.start(10)
    time.sleep(3)
    p.ChangeDutyCycle(19)
    time.sleep(5)
    p.stop()
    GPIO.cleanup() 

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    p.stop()
    GPIO.cleanup() 