import pyshark

msg = []

for pkt in pyshark.FileCapture("capture.pcap"):
    if pkt.ip.src == "172.18.4.3" and "smb" in pkt:
        cmd = int(pkt.smb.cmd)
        if cmd == 0x2f or cmd == 0x32:
            padding = pkt.smb.padding.replace(":", "")
            padding = bytes.fromhex(padding).lstrip(b"\x00")
            msg.append(padding)

msg = b"".join(msg).decode()
print(msg)
