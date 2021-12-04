# Summary
- Takeaways:
    - after initial foothold, any way to write to the target and trigger a reverse shell will likely be useful (e.g., being able to edit the Joomla template in order to trigger a reverse shell)
- User: directory and webpage enumeration to retrieve username and password for Joomla instance, then editing Joomla template and setting it to the default to trigger a reverse shell, then decompressing a series of files to reveal the SSH password for `floris`
- Root: recurring `curl` command made by the `root` user which reads in a config file that is editable by `floris`, permits overwriting the `/etc/passwd` file with a new one that includes a new user with root access and a known password

# Details
### User: 65dd1df0713b40d88ead98cf11b8530b
- Nmap scan reveals ports 22 and 80 are open
- directory enumeration reveals `secret.txt` (which contains a base64 encoded string that decodes to `Curling2018!`) and a `Joomla` administrator login located at `/administrator`
- posts on the website are written by `Super User`, but one of them is signed `Floris`
- using `username: floris` and `password: Curling2018!` permits logging into both the website and the `Joomla` web interface
- inside the `Joomla` web interface, it's possible to edit the templates used to render the webpages and change the default template
- place a reverse shell in `index.php` of the template not currently in use, start a listener, then switch the default template to the one with the reverse shell and reload `index.php`
- the reverse shell will spawn as user `www-data` who can read a file named `password_backup` in `/home/floris`
- using `xxd` to reverse the hexdump in `password_backup` and then a series of decompressions (`bunzip2`, `gunzip`, and `tar`) makes it possible to retrieve the SSH password (`5d<wdCbdZu)|hChXll`) for `floris`

### Root: 82c198ab6fc5365fdc6da2ee5c26064a
- using `pspy64` reveals that `root` user occasionally runs `/bin/sh -c curl -K /home/floris/admin-area/input -o /home/floris/admin-area/report`, where it reads a `curl` command from a config file using the `-K` option
- user `floris` has the ability to write to the `/home/floris/admin-area/input` file and can control all the components of the `curl` call
- possible to copy the `/etc/passwd` file, append a new user with root permissions and a password generated with `openssl passwd`, and then edit the config file to have the curl command retrieve the edited file (`url = "http://127.0.0.1:8000/passwd"`) and overwrite the real file (`output = "/etc/passwd"`)
- example above uses `python3 -m http.server` from the target machine to serve the edited file right back to the `curl` command made by `root`

### References:
- https://www.hackingarticles.in/joomla-reverse-shell/
