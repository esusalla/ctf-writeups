# Summary
- Takeaways:
	- recognize the signs of a sandbox or jail sooner (presence of `.dockerenv`, missing usual binaries, local IP address, unable to SSH in, `/assets` directory in root, flag(s) not in usual location, etc.)
	- using targeted `find` commands along with the `vi` directory browser makes for more efficient enumerating
- User: Gitlab 11.4.7 RCE vulnerability to get user within Docker container
- Root: `root` password in a config file, escalate then break out of Docker container by mounting `/dev/sda2` directly (have access to `fdisk` as `root`)

# Details
### User
- scan reveals port 22 and 5080 open
- 5080 is hosting a Gitlab instance that allows you to create an account
- after logging in, it can be seen it's Gitlab 11.4.7
- searching for this reveals an RCE exploit that takes advantage of SSRF and CRLF vulnerabilities to achieve command execution
- use repository import feature (with IPv6 trick to bypass localhost filtering) to make a request to the local redis instance
- use the CRLF vulnerability to inject multiple commands into redis without it terminating due to the "Host" HTTP header
- reverse shell allows you to read user flag
- https://github.com/ctrlsam/GitLab-11.4.7-RCE/blob/master/exploit.py

### Root
- unable to directly SSH in even after writing `authorized_keys` due to Docker container sandbox
- use `find` to locate the `python` binary that is embedded with the gitlab install (rather than on the usual path) and use it to get better shell
- enumerating reveals a number of directories and files related to the Gitlab install
- there is a `backups` directory located at `/opt/backups` that contains a gitlab config file with one line uncommented and changed (SMTP password line)
- can use the same password to `su` as `root`
- `.dockerenv` in root directory along with `/assets` folder and lack of `/root/root.txt` points to a Docker container escape
- running `fdisk -l` reveals the container was likely spawned with the `--privileged` flag which gives it access to the host's devices
- this allows you to directly mount the main harddrive and use it to escape the sandbox
- https://book.hacktricks.xyz/linux-unix/privilege-escalation/docker-breakout
