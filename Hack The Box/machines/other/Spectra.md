# Summary
- Takeaways:
	- holistic view of filesystem is necessary for efficient and complete enumeration (possibly mount with sshfs or find / develop tooling)
	- can get around "noexec" mount restrictions by calling scripts with `bash` rather than directly (e.g. `/bin/bash <script name>`)
	- use `wpscan` for WordPress installations
- User: find WordPress login credentials, use admin privileges to edit plugin and achieve RCE before finding creds in `/etc/autologin/passwd` file and pivoting to user
- Root: user is able to run `/sbin/initctl` with sudo while also being able to edit system job files in `/etc/init` leading to arbitrary command execution as `root`

# Details
### User
- ports 22, 80, and 3306 are open with a message on the website about the dev team setting up a Jira tracker
- directory enumeration reveals /testing and /main endpoints with the /testing directory including a `wp-config.php.save` that makes the database credentials readable
- WordPress install located at /main endpoint, making it possible to log in as `administrator` with the `devteam01` password from the `wp-config.php.save` under /testing
- once logged it, it's possible to directly edit one of the plugins so that it executes commands from the URL parameter, allowing you to write an SSH key to `nginx` user's home directory and SSH in
- further enumeration reveals a script under `/opt/autologin.conf.orig` that checks for a `passwd` file located at `/etc/autologin/passwd`
	- decently hard to notice, better file system navigation would help, file looks like actual piece of OS (and believe it is), so initially didn't raise enough suspicions
- password for user `katie` found in `/etc/autologin/passwd` (`SummerHereWeCome!!`)

### Root
- `katie` is able to run `/sbin/initctl` with sudo while also setting environment variables (didn't use this functionality)
- `katie` also belongs to the `developers` group which owns several Upstart job files in `/etc/init`, which makes it possible for `katie` to edit them and insert any arbitrary commands
- writing a reverse shell into one of the job files owned by the `developers` group and then running it with `sudo /sbin/initctl start test.conf` gives root access

#### Tags: ChromeOS
