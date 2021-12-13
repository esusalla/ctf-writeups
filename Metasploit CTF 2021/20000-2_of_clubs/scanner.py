from scapy.all import *


def scan(pkt):
    if TCP in pkt:

        data = str(pkt[TCP].payload)
        print("src host:", pkt[IP].src)
        print("dst host:", pkt[IP].dst)

        print("src port:", pkt[TCP].sport)
        print("dst port:", pkt[TCP].dport)

        print(data + "\n")
        

sniff(filter="host 10.0.2.15", prn=scan)
