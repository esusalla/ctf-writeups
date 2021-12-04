# Summary
- User: web app is vulnerable to Drupalgeddon2 exploit (CVE-2018-7600), creds to escalate in SQL database
- Root: install custom malicious snap with sudo permissions to run arbitary commands as root 

# Details
### User
- port scan reveals ports 22 and 80 are open
- website enumeration reveals it's a Drupal install, MAINTAINERS.txt file indicates likely around version 7 or 8
- searching for Drupal exploits with `searchsploit` reveals a Form API exploit named Drupalgeddon2 that gives RCE
	- https://research.checkpoint.com/2018/uncovering-drupalgeddon-2/
	- https://github.com/dreadlocked/Drupalgeddon2
- Ruby script can be used to achieve shell access as `apache` user
- stuck in sandbox as `apache`, but possible to `grep` through files in directory for any mention of "password"
- able to retrieve the `drupaluser`	password for the MySQL Drupal database
- retrieving the `users` table from the `drupal` database gives a hash that can be cracked to reveal `brucetherealadmin`'s password (`booboo`)
- able to SSH in with cracked password

### Root
- `brucetherealadmin` is able to run `/usr/bin/snap install *` as root
- possible to craft a custom malicious snap that executes a command using the install hook functionality
	- https://gtfobins.github.io/gtfobins/snap/
	- change name of snap ("x" in example) when using
- having trouble with external connectivity, but able to create /root/.ssh and insert public key into authorized_keys
