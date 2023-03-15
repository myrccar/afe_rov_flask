#!/usr/bin/env python

# servo_demo.py
# 2016-10-07
# Public Domain

# servo_demo.py          # Send servo pulses to GPIO 4.
# servo_demo.py 23 24 25 # Send servo pulses to GPIO 23, 24, 25.

import sys
import time
import random
import pigpio

NUM_GPIO=32

MIN_WIDTH=1000
MAX_WIDTH=2000

step = [0]*NUM_GPIO
width = [0]*NUM_GPIO
used = [False]*NUM_GPIO

pi = pigpio.pi()

if not pi.connected:
   exit()

if len(sys.argv) == 1:
   G = [4]
else:
   G = []
   for a in sys.argv[1:]:
      G.append(int(a))
   

print("Sending servos pulses to GPIO {}, control C to stop.".
   format(' '.join(str(g) for g in G)))

pi.set_servo_pulsewidth(G[0],1500)
time.sleep(2.5)

while True:

   try:
    
    pi.set_servo_pulsewidth(G[0],1700)
    time.sleep(0.1)
    
   except KeyboardInterrupt:
      break

print("\nTidying up")

for g in G:
   pi.set_servo_pulsewidth(g, 0)

pi.stop()

