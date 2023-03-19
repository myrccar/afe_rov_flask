import requests
import json
import pigpio
import time
import asyncio

pi = pigpio.pi()

"""
rov_pi.py:
gets controller data use the control_i.py api
run motors(later)
"""

print("inisliseing ese 13,12,18,19 4s")
pi.set_servo_pulsewidth(13,1500)
pi.set_servo_pulsewidth(12,1500)
pi.set_servo_pulsewidth(18,1500)
pi.set_servo_pulsewidth(19,1500)
time.sleep(4)
print("done")

old_min = -1.0
old_max = 1.0
min_pwm = 1430
max_pwm = 1600
max_delta = 100
pwm_stop = 1500

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

def convert_controller(old_value):
    return int(clamp(pwm_stop + (max_delta * old_value),min_pwm,max_pwm))

def tank_steering(horizontal, vertical):
    left = convert_controller((vertical - horizontal))
    right = convert_controller(vertical + horizontal)
    print(horizontal,vertical)
    return (left, right)



try:
    while True:
        r = requests.get("http://192.168.0.98",verify=False)
        data=r.json()
        #update escs
        pi.set_servo_pulsewidth(18,convert_controller(data['axis-4']))
        pi.set_servo_pulsewidth(13,convert_controller(data['axis-3']))
        left,right = tank_steering(data['axis-0'],data['axis-1'])
        print(left,right)
        pi.set_servo_pulsewidth(19,left)
        pi.set_servo_pulsewidth(12,right)
        

        


except KeyboardInterrupt:
    print("ctrl+c")