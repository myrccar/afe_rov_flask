from flask import Flask
import xbox

"""
control_pi.py:
this script is a api made with flask that returns
json data with controller inputs

made by myrccar
"""


app = Flask(__name__)
joy = xbox.Joystick()

@app.route('/')
def data():
    controller_data = {
        "axis-0":joy.leftX(),
        "axis-1":joy.leftY(),
        "axis-2":joy.leftTrigger(),
        "axis-3":joy.rightX(),
        "axis-4":joy.rightY(),
        "axis-5":joy.rightTrigger(),
        "button-1":joy.B(),
        "button-2":joy.X(),
        "button-3":joy.Y(),
        "button-0":joy.A()
    }

    return controller_data


if __name__ == '__main__':
    app.run(host="192.168.0.98",port=80)