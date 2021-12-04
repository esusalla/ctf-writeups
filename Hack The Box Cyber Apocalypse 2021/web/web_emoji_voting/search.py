import readline

import requests

if __name__ == "__main__":
    URL = "http://localhost:1337/api/list"
    HEADERS = {"Content-Type": "application/json"}

    while True:
        order = input("order: ")

        res = requests.post(URL, headers=HEADERS, json={"order": order})
        print(res.text)
