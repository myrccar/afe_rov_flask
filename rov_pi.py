import requests
import json
import pigpio
import time

pi = pigpio.pi()

"""
rov_pi.py:
gets controller data use the control_i.py api
run motors(later)
"""

print("inisliseing ese 13,12,18,19 4s")
pi.set_servo_pulsewidth(13,1500)
# pi.set_servo_pulsewidth(12,1500)
# pi.set_servo_pulsewidth(18,1500)
# pi.set_servo_pulsewidth(19,1500)
time.sleep(4)
print("done")

old_min = -1.0
old_max = 1.0
min_pwm = 1300
max_pwm = 1700


def convert_controller(old_value):
    old_range = old_max - old_min
    new_range = max_pwm - min_pwm
    new_value = ( (old_value - old_min) / (old_max - old_min) ) * (max_pwm - min_pwm) + min_pwm
    return int(new_value * 1)


try:
    while True:
        r = requests.get("http://192.168.0.98",verify=False)
        data=r.json()
        #update escs
        pi.set_servo_pulsewidth(18,convert_controller(data['axis-4']))

        


except KeyboardInterrupt:
    print("ctrl+c")