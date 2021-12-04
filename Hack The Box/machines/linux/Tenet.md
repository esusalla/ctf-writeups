# Summary
- Takeaways:
	- inspect box logo / image for early hints and directions
- User: PHP deserialization leading to webshell and then creds in config
- Root: race condition with script running as `root`

# Details
### User
- posting on the website mentions moving from a flat to a more robust directory structure
- another user asked if the `sator php` or the backup had already been moved
- trying to navigate directly to the IP address rather than the `tenet.htb` host reveals that the Apache server is serving the WordPress parent directory as well
- enumerating this directory reveals a `users.txt` file, while navigating to `/sator.php` and `/sator.php.bak` reveal hits
- able to retrieve `/sator.php.bak` and see that it deserializes a user provided object and there's also a class in scope that uses the magic `__destructor` function
- possible to create and serialize a malicious object that changes the data and file to be written to, making it possible to write a webshell into the WordPress directory and get a shell on the box
- reading the `wp-config.php` file reveals the password for user `neil`

### Root
- `sudo -l` reveals `neil` can run an `enableSSH.sh` script as root that writes a key into `/root/.ssh/authorized_keys`
- the script first creates a temp file, then makes sure the file exists and is zero bytes, it then writes the key to the file and the writes that file into `authorized_keys`
- can't just detect the temp filename and try to spam overwrite it with our key because the script does a check to make sure the file is empty
- have to take measurements on how long the temp file stays around and then attempt to overwrite with our public key towards the end of it's existence (trying to get in between the file check and the subsequent writing to `authorized_keys`)
- successfully timing it allows you to login in as `root`
