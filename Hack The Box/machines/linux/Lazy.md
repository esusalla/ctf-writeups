# Summary
- Takeaways:
    - tamper with cookies to check padding and see if they would be vulnerable to `padbuster`
    - SUID binaries or anything run by `root` that internally calls a program with a relative path may be vulnerable to having that program name shadowed with another program that takes precedence over it in the `PATH` variable
- User: brute-force admin login, then download private SSH key and use it to log in
- Root: SUID binary that runs as root uses a program (`cat`) with a relative pathname, meaning a fake script with the same name can be created to spawn a shell and then the path to it can be appened to the front of the `PATH` variable to get it to execute

# Details
### User: d558e7924bdfe31266ec96b007dc63fc
- Nmap scan reveals ports 22 and 80 are open
- there's are login and registration forms, and attempting to register as `admin` returns a message that the user already exists
- fuzzing the login form using `wfuzz -c -z file,pwds.txt -d "username=admin&password=FUZZ" --hh 1629 -u http://lazy.htb/login.php` with the first 50,000 lines of rockyou.txt reveals the admin password to be `p4ssw0rd`
- after logging in with the password, an SSH key is available for download that states it is meant to be used with the user `mitsos`
- logging in over SSH with the key grants access to the user flag

#### Alernate routes:
- use `padbuster` on the cookie in order to break the encryption and change the user to `admin` and re-encrypt the cookie to achieve access
 
### Root: 990b142c3cefd46a5e7d61f678d45515
- `backup` file in home directory is an SUID binary that runs as root
- the program calls `cat` with a relative pathname
- another file named `cat` which executes a shell can be created and then the path to it can be added to the front of the `PATH` variable so that it gets called whenever `backup` is executed
