# Summary
- Takeaways:
	- when using FTP, make sure to use `ls -al` to view all files and directories (missed directories that are hidden by default on Windows, e.g., `/ProgramData` and `/Users/All User`)
	- when looking for application data on Windows, check `/Users/All User/Application Data/<application>`
	- make sure to pull all versions of files and check for loot (didn't pull the old config backup at first, which ended up containing the password)
	- when passwords contain obvious years, always try incrementing and decrementing them when attempting authentication
- User: able to anonymously login with FTP and read the user flag
- Root: find credentials before exploiting an authenticated RCE vulnerability to escalate privileges

# Details
### User
- scan reveals ports 21, 80, 135, 139, 445, and 5985 are open (along with several in the 47000+ range for Windows RPC)
- attempting to log in to the FTP anonymously reveals you're dropped into the server's root directory and able to access almost everything

### Root
- the website on port 80 is running `PRTG Network Monitoring` software
- there is a RCE exploit available for the version running, but it requires authentication
- default credentials don't work, and searching for where credentials are stored reveals they're in `%ALLUSERSPROFILE%\Application Data\Paessler\PRTG Network Monitor`
- pulling both the config and the backup and searching them for the default username of `prtgadmin` reveals the password in `PRTG Configuration.old.bak` is `PrTg@dmin2018`
- trying to login with `prtgadmin:PrTg@dmin2018` doesn't work, but incrementing the year and trying `prtgadmin:PrTg@dmin2019` permits logging in
- once logged in, we can use CVE-2018-9276 to create a new malicious notification and then trigger it to achieve RCE and open a reverse shell as `administrator`
- https://github.com/wildkindcc/CVE-2018-9276
