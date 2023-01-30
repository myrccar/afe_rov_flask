import requests
import json
import RPi.GPIO as GPIO  

"""
rov_pi.py:
gets controller data use the control_i.py api
run motors(later)
"""

GPIO.setmode(GPIO.BOARD)             # choose BCM or ---BOARD(one we use)---  
GPIO.setup(12, GPIO.OUT)

try:
    while True:
        r = requests.get("http://192.168.0.98",verify=False)
        data=r.json()
        GPIO.output(12,data["button-0"])


except KeyboardInterrupt:
    GPIO.cleanup()