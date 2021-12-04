# Summary
- Takeaways:
	- always try username as password when testing creds
	- sometimes helps to try exploits that are supposed to be patched in the current version of the service if there aren't other obvious paths
	- add UDP scan to default scans to avoid missing things in the future
	- always attempt to read non-standard scripts found on server
- User: retrieve server information with `snmpwalk`, login to SeedDMS and leak database creds, then use those to upload SSH key through Cockpit
- Root: folder with ACL privileges that allow you to create files which are run by `root` whenever `snmpwalk` is used

# Details
### User
- port scan reveals ports 22, 80 and 9090 are open along with UDP port 161 (SNMP)
- port 80 holds a default Nginx server page while port 9090 hosts a Cockpit service
- using `snmpwalk -v 2c -c public pit.htb .1` returns information that reveals the existense of `/var/www/html/seeddms51x/seeddms` along with username `michelle`
- Cockpit service uses HTTPS with certificate that has a common name of `dms-pit.htb`
- using this information to navigate to `dms-pit.htb/seeddms51x/seeddms` reveals a login page that can be authenticated to with `michelle:michelle`
- once logged in, you can use an RCE exploit that is supposed to be patched in the current version, but reverse shells aren't possible
- you can still read files on the server, allowing you to retrieve the SeedDMS config file which contains database creds
- using the database password with username `michelle` allows you to login tothe Cockpit service and add an SSH key
- can now SSH in as `michelle` and retrieve the user flag

### Root
- `snmpwalk` also revealed the existence of a `/usr/bin/monitor` file that appears to be run whenever `snmpwalk` is used to get information from the server
- can't execute the script, but can read it to see that it runs all the files in the `/usr/local/monitoring` directory that have the formation `check*sh`
- this directory has permissions that are controlled with an ACL which permits us to write to the directory
- can create a script that writes a public key to `/root/.ssh/authorized_keys` whenver it's ran, then make it executable and copy it into the `/usr/local/monitoring` directory
- after calling `snmpwalk` with ther server as the target, `root` will run `/usr/bin/monitor` and call the script, allowing you to SSH as `root` and retrieve flag

#### Tags: snmpwalk 
