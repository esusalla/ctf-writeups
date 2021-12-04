# Summary
- Takeaways:
    - use `jd-gui` to view details and classes within `.jar` files (can also unzip them to view the files inside and decompile them with `jadx-gui`)
- User: `/plugins` endpoint contains a `.jar` file with credentials inside that can be used to authenticate with `phpMyAdmin`, then within `phpMyAdmin` the `wordpress` database can be read to reveal a user named `notch` exists, SSH in with `notch` and the password from the `.jar` file
- Root: user has full sudo privileges and can simply spawn a root shell

# Details
### User: 59fee0977fb60b8a0bc6e41e751f3cd5
- Nmap scan reveals ports 21, 22, 80 and 25565 (Minecraft) are open
- the main page on the website mentions a "wiki" in the works, and directory enumeration reveals a `/wiki` enpoint
- the `/wiki` endpoint mentions "plugins", which also has a corresponding endpoint at `/plugins`
- navigating to `/plugins` reveals two `.jar` files available for download
- analzying `BlockyCore.jar` with `jd-gui` shows the class within contains SQL credentials (`username: root` and `password: 8YsqfCTnvxAUeduzjNSXe22`)
- the above credentials can be used to login to the `phpMyAdmin` webportal located at `/phpmyadmin`
- the `wordpress` database can be accessed within phpMyAdmin, which contains a `wp-users` table with a hashed password (`$P$BiVoTj899ItS1EZnMhqeqVbrZI4Oq0/`) for `notch`
- the password can't be cracked by `john`, but it's possible to login over SSH with `username: notch` and `password: 8YsqfCTnvxAUeduzjNSXe22`

#### Alernate routes:
- possible to change the password for user `notch` within the `wordpress` table in order to login to the WordPress as an admin, upload a reverse PHP shell, and get access through there, but then there's no way to escalate

### Root: 0a9694a5b4d272c694679f7860f1cd5f
- using `sudo -l` with the password used to log in reveals user `notch` is able to run any command as `root` and can run `sudo /bin/bash` in order to get a root shell
