# Summary
- User: msfvenom APK parser command injection to achieve user shell
- Root: pivot through log file command injection and elevate using sudo access to msfconsole

# Details
### User
- port scan reveals ports 22 and 5000 are open
- port 5000 contains a script kiddie shell that can run nmap, msfvenom, and searchsploit
- can't command inject on the nmap or searchsploit commands, but the msfvenom command will also make Android APK's and is vulnerable to command injection through msfvenom template use (CVE-2020-7384)
	-  https://github.com/justinsteven/advisories/blob/master/2020_metasploit_msfvenom_apk_template_cmdi.md
-  use exploit script to craft a malicious template that includes a reverse shell command in the dname field (which gets passed to Popen as a full string by the msfvenom apk parser)
- get shell as `kid` user

### Root
- can view a script that runs in `pwn` user's home directory that parses a log file under control by `kid` user and then uses the third field as an IP input to an nmap command that is not escaped
- can include another reverse shell payload in the log file in order to achieve shell access as `pwn`
- checking `sudo -l` as `pwn` reveals they can run `msfconsole` as the `root` user
- once in `msfconsole` as `root`, you can also run normal shell commands with the elevated privileges
