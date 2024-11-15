import requests
import json
import pigpio
import time
import asyncio

pi = pigpio.pi()

"""
rov_pi.py:
gets controller data use the control_pi.py api
run motors
"""


#todo new func innit or something
print("initializing ese 13,12,18,19. please wait 4+ seconds")
pi.set_servo_pulsewidth(13,1500)
pi.set_servo_pulsewidth(12,1500)
pi.set_servo_pulsewidth(18,1500)
pi.set_servo_pulsewidth(19,1500)
time.sleep(4)
print("done initializing")

old_min = -1.0
old_max = 1.0
min_pwm = 1430
max_pwm = 1600
max_delta = 100
pwm_stop = 1500

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

def adjust_controller_single(old_value):
    return int(clamp(pwm_stop + (max_delta * old_value),min_pwm,max_pwm))

def tank_steering(horizontal, vertical):
    left = adjust_controller_single((vertical - horizontal))
    right = adjust_controller_single(-(vertical + horizontal))
    return (left, right)

def reconnect():
    stop()
    main()

def stop():
    pi.set_servo_pulsewidth(13,1500)
    pi.set_servo_pulsewidth(12,1500)
    pi.set_servo_pulsewidth(18,1500)
    pi.set_servo_pulsewidth(19,1500)


def main():
    try:
        while True:
            data = requests.get("http://192.168.0.98",verify=False,timeout=0.6).json()
            #update escs
            pi.set_servo_pulsewidth(18,adjust_controller_single(data['axis-4']))
            pi.set_servo_pulsewidth(13,adjust_controller_single(data['axis-3']))
            left,right = tank_steering(data['axis-0'],data['axis-1'])
            pi.set_servo_pulsewidth(19,left)
            pi.set_servo_pulsewidth(12,right)
        
    except KeyboardInterrupt:
        print("program stop by keyboard input, gracefully exiting...")
        stop()
    except Exception as e:
        print("program crashed! error: \n {e} \n attempting to reconnect...")
        reconnect()

