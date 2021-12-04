import readline

import requests

if __name__ == "__main__":
    URL = "http://localhost:1337/search"
    HEADERS = {"Content-Type": "application/xml"}

    while True:
        query = input("query: ")
        xml = '<?xml version="1.0" encoding="ISO-8859-1"?>' + query
        print(xml)
        
        res = requests.post(URL, headers=HEADERS, data=xml)
        print(res.text)
