import readline

import requests

URL = "http://localhost:1337/change_status"

while True:
    inj = input("inj: ")
    res = requests.post(URL, auth=("admin", "admin"), json={"cameras": inj})
    print(res.text)
