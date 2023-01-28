from flask import Flask

"""
control_pi.py:
this script is a api made with flask that returns
json data with controller inputs

made by myrccar
"""


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()