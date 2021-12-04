import os
import pathlib
import socket
import subprocess
import threading


def handle_client(conn):
    proc = subprocess.Popen(f"{DIR}/nx-oopsie", stdin=conn, stdout=conn, stderr=conn)
    print(f"Process {proc.pid} started", flush=True)
    proc.communicate()
    print(f"Process {proc.pid} exited with {proc.returncode}", flush=True)
    conn.close()


if __name__ == "__main__":
    DIR = pathlib.Path(__file__).parent.absolute()
    PORT = 8001

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # If running within Docker, use default Docker container IP
    if os.path.exists("/.dockerenv"):
        sock.bind(("172.17.0.2", PORT))
    else:
        sock.bind(("127.0.0.1", PORT))

    sock.listen()
    print(f"Python app server listening on port {PORT}...", flush=True)

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

