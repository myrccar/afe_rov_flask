from flask import Flask
import xbox
import time
import logging
import threading
#import RPi.GPIO as GPIO
#install gpio on pi: 
# sudo apt-get install python-dev
# sudo apt-get install python-rpi.gpio

print("hi i'm running")
"""
control_pi.py:
this script is an API made with Flask that returns
JSON data with controller inputs

made by myrccar
"""

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(40, GPIO.OUT)

app = Flask(__name__)
joy = None
while joy is None:
    try:
        joy = xbox.Joystick()
    except:
        print("waiting for joystick, please connect one")
        time.sleep(1)

print("joystick connected. starting server")

CLAW_TOGGLE = False

# Configure logging
log_handler = logging.FileHandler("app.log")
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

# Shared data structure and lock
controller_data = {}
data_lock = threading.Lock()

def update_joystick_data():
    global controller_data
    while True:
        try:
            axes = {
                "left_x": joy.leftX(),
                "left_y": joy.leftY(),
                "right_x": joy.rightX(),
                "right_y": joy.rightY(),
                "left_trigger": joy.leftTrigger(),
                "right_trigger": joy.rightTrigger()
            }
            
            buttons = {
                "button-0": joy.A(), 
                "button-1": joy.B(), 
                "button-2": joy.X(), 
                "button-3": joy.Y()  
            }
            
            with data_lock:  # Acquire lock before updating shared data
                controller_data = {
                    "axis-0": axes["left_x"],
                    "axis-1": axes["left_y"],
                    "axis-2": axes["left_trigger"],
                    "axis-3": axes["right_x"],
                    "axis-4": axes["right_y"],
                    "axis-5": axes["right_trigger"],
                    "button-0": buttons["button-0"],
                    "button-1": buttons["button-1"],
                    "button-2": buttons["button-2"],
                    "button-3": buttons["button-3"]
                }
            
            logger.debug(f"Joystick data updated: {controller_data}")
        except Exception as e:
            logger.exception(f"Error reading joystick data: {e}")
        
        time.sleep(0.5)  # Polling interval of 0.5 seconds

# Start the joystick data update thread
joystick_thread = threading.Thread(target=update_joystick_data, daemon=True)  # daemon=True for background thread
joystick_thread.start()

@app.route('/')
def data():
    with data_lock:  # Acquire lock before reading shared data
        current_data = controller_data.copy()  # Create a copy to avoid thread issues
    return current_data

if __name__ == '__main__':
    try:
        logger.info("Application started")
        app.run(host="192.168.0.98", port=80)
    except Exception as e:
        logger.exception(f"An exception occurred during app startup: {e}")
    finally:
        logger.info("Application shutting down")
        joy.close()  # Ensure joystick is closed when the app exits
