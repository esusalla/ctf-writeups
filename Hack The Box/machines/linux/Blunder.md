 Summary
- Takeaways:
    - remember to Google specific problems, even if results seem unlikely it's worth a shot (e.g., `bludit brute force bypass`)
    - `cewl` can be used to generate custom wordlists from webpage content
- User: directory enumeration, custom wordlist generation, file upload exploit in Bludit, and cracking a password hash found in a web directory
- Root: exploit to circumvent the `sudo` permission `(ALL, !root) /bin/bash` by referring to `root` as "-1" rather than "root" or "0"

# Details
### User: 9f6a80e7c5e64f20130603a2672895f0
- Nmap scan reveals ports 21 closed (accessible, but no application listening on it) and 80 are open
- using `gobuster` with `txt` extension discovers `blunder.htb/todo.txt` that mentions a `fergus` user
- use `cewl -d 3 -m 4 -w wordlist.txt` to generate a wordlist based on the website
- brute force login to the admin panel located at `blunder.htb/admin` with username `fergus`, generated wordlist, and Bludit brute force rate-limiting bypass exploit
    - https://rastating.github.io/bludit-brute-force-mitigation-bypass/
- brute force reveals password for `fergus` is `RolandDeschain`
- use `metasploit => exploit/linux/http/bludit_upload_images_exec` with login creds to gain shell access on the target
- navigate up out of the `/var/www/bludit-3.9.2/bl-content/tmp` and into `/var/www/bludit-3.10.0a/bl-content/databases`, then read `users.php` to reveal hashed password for `hugo`
- crack hash to reveal `Password120` as password for `hugo`
    - https://crackstation.net/

### Root: c6d9c5843eaa3b9d4007b476c99c7a3d
- `sudo -l` with `hugo`'s password reveals they can run `/bin/bash` as every user except `root`, permitting the switch to user `shaun`
- use an exploit that circumvents the no `root` restriction by using the ID "-1" or "4294967295" instead of "0" or "root"
    - `sudo -u#-1 /bin/bash`
    - https://www.networkworld.com/article/3446036/linux-sudo-flaw-can-lead-to-unauthorized-privileges.html
