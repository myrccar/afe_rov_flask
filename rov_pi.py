import requests
import json

"""
rov_pi.py:
gets controller data use the control_i.py api
run motors(later)
"""

while True:
    r = requests.get("http://localhost:5000/")
    data=r.json()
    print(data)