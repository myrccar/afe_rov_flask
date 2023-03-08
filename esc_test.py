"""
a script to test the esc/motors on the rov pi
"""
import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

# Set up PWM
pwm = GPIO.PWM(12, 50)
pwm.start(0)

# Set speed to 50%
pwm.ChangeDutyCycle(50)
time.sleep(5)

# Stop PWM
pwm.stop()

# Clean up GPIO
GPIO.cleanup()


