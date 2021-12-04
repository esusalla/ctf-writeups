# Summary
- Takeaways: 
    - check for custom / non-typical SUID binaries (use `suid3num.py` or closely check `linpeas.sh` "Interesting Files" section)
    - scripts running other scripts or commands using a relative filepath can be shadowed and taken control of by adjusting the PATH environment variable
- User: SQL injection followed by PHP smuggling in an image file, credential harvesting from the webroot directory, and dumping the SQL database for additional credentials
- Root: locate non-typical binary with SUID capability and shadow scripts called by it with custom scripts with the same name to achieve arbitrary command execution

# Details
### User: aabd03e7f45f26d4f01929c97e350761
- Nmap scan reveals ports 22 and 80 are open
- `magic.htb/login.php` has a login form vulnerable to SQL injection
    - `username=admin';&password=`
- add JPG magic bytes to start of PHP reverse shell, upload, and trigger it by navigating to `magic.htb/images/uploads/kitten.jpg.php`
- `/var/www/Magic/db.php5` reveals the MySQL password for `theseus` is `iamkingtheseus`
- `mysql` not present on system, so use `mysqldump --all-databases -u theseus -p` with password `iamkingtheseus` to dump the database and reveal the `admin` password to be `Th3s3usW4sK1ng`
- `su` into user `theseus` using `Th3s3usW4sK1ng` password

### Root: cd4a125948f1a4b9d4e14cd77a128ed1
- optionally add SSH key for SSH access
- enumeration (specifically with `suid3num.py` and `linpeas.sh`) reveals an interesting SUID file located at `/bin/sysinfo`
- running `strings` on the file and monitoring `pspy64` while running it shows it called several relative functions / scripts during execution (e.g., `lshw`, `fdisk`, `cat`, and `free`)
- adjusting the `PATH` environment variable and adding custom scripts with the same names as the ones listed above allow for arbitray command execute as `root`
