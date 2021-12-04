# Summary
- Takeaways:
    - try all known username and password combinations when attempting to authenticate with any service
    - possible to copy files out of directories with execute-only permissions if the name of the file is known
    - socat can be used for local port forwarding if unable to set it up through SSH (e.g., `socat TCP4-LISTEN:8080,fork TCP4:127.0.0.1:8443`)
    - make sure to look closely for non-default files in home directories
- User: Wordpress plugin LFI leading to discovery of creds in config files and virtual host with RCE through SQL injection, password in user's home directory (partially protected in execute-only directory)
- Root: Java deserialization leading to RCE, "cap\_sys\_module" permissions in Docker container allows inserting reverse shell kernel module into host

# Details

### User
- port scan reveals ports 22 and 80 are open
- port 80 hosts a WordPress website
- using `wpscan` reveals the site uses a plugin with a LFI vulnerability
    - https://www.exploit-db.com/exploits/44544
    - http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=/../../../../
- possible to read the default Apache config to reveal any virtual hosts and their root directories (`/etc/apache2/sites-enabled/000-default.conf`)
- can then examine the config files for any credentials
    - monitors.htb => /var/www/wordpress/wp-config.php
    - cacti-admin.monitors.htb => /usr/share/cacti/cacti/include/config.php
- WordPress config contains a password than can be used along with the "admin" user name to log into the Cacti service
- once inside the Cacti service, it's possible to use an SQL injection vulnerability to write a new reverse shell command into the "path\_php\_binary" which will be executed as the "www-data" user
    - https://www.exploit-db.com/exploits/49810
- after obtaining a foothold, it can be found that the box lacks `curl` and `wget`, but can still download external scripts using Python
- `linpeas.sh` reveals that a service unit is calling a script located in `marcus`'s home directory, "/home/marcus/.backup/backup.sh"
- the "/home/marcus/.backup" directory is execute only so the files can't be read directly, but they can be copied out of it if their full paths are known
- copying the "backup.sh" scripts allows you to read it, retrieve the password for `marcus`, and SSH in

### Root
- "note.txt" in `marcus`'s home directory mentions setting up the Docker container for production
- runnning `netstat -tunlvp` reveals there is a service listening on 127.0.0.1:8443, and `ps aux` also shows `docker-proxy` is sending those connections to a Docker container
- port 8443 is often used by Tomcat SSL connections
- forwarding the port for remote access shows that the site is hosting an Apache OFBiz instance (suite of business applications)
- searching for exploits reveals there are some Java deserialization vulnerabilities that lead to RCE
	- https://www.zerodayinitiative.com/blog/2020/9/14/cve-2020-9496-rce-in-apache-ofbiz-xmlrpc-via-deserialization-of-untrusted-data
	- https://github.com/cyber-niz/CVE-2020-9496
- possible to use `metasploit` module to achieve a reverse shell in the Docker container as `root`
    - module => `exploit/linux/http/apache_ofbiz_deserialization`
    - have to enable ForceExploit setting for it to work
- checking permissions with `capsh --print` reveals that the container has the `cap_sys_module` capability and can insert kernel modules into the host machine
- both the host machine and the container are runnning the same version of Ubuntu, so it's possible to compile the reverse shell kernel module right in the container and then insert it with `insmod` to achieve a reverse shell as root on the host
    - https://blog.pentesteracademy.com/abusing-sys-module-capability-to-perform-docker-container-breakout-cf5c29956edd

#### Tags: LFI, SQL injection, Java deserialization, Docker escape (cap\_sys\_module)
