# Summary
- Takeaways:
	- JSON web token headers are completely under the control of the client when sending back, only the data is signed
	- possible to specify a key to use with the "kid" header field (still up to the server regarding what to do with that value)
- User: forge admin JWT, upload web shell, retrieve creds from backup
- Root: breakout of Docker container via `runc` (CVE-2019-5736)

# Details
### User
- scan reveals port 22 and 80 open
- website allows you to make notes
- not vulnerable to any injection attacks, but note count starts at 6 and it's not possible to read the earlier ones
- trying to login as `admin` alerts you that it already exists
- server sends a JSON web token along that contains "username", "email", and "admin_cap" fields
- header of JWT contains a key identification field "kid" showing that it points to "http://localhost:7070" (presumably it makes a request to this endpoint in order to retrieve the key for checking the validity of the JWT)
- possible to change the header to a user-controlled key hosted locally and forge a JWT that elevates you to admin and allows you to read their notes
- notes point to the ability to upload a PHP file as well as recent backups
- admin account has file upload capability so it's possible to directly upload a PHP webshell
- once on the server, there's a backup of `noah`s home directory in `/var/backups` that contains their private RSA key and allows you to SSH in

### Root
- `sudo -l` reveals `noah` can run `docker exec -it webapp-dev01*`, allowing them to run any command on the webapp-dev01 container
- possible to breakout of Docker and attain root on the host machine by exploiting vulnerable version of `runc`
- when `docker exec` spawns a process inside of a container, `runc` places itself inside the container and then forks off the new process
- possible to make a binary in the container point to `/proc/self/exe` so that `runc` places a copy of itself into the container
- then possible to find that process and open it within the container before using the file descriptor to overwrite it (which is the `runc` on the host machine) with a new command
- possible to overwrite it with reverse shell code that will execute as `root` on the host machine
- https://unit42.paloaltonetworks.com/breaking-docker-via-runc-explaining-cve-2019-5736/
- https://github.com/Frichetten/CVE-2019-5736-PoC

#### Tags: JSON web token (JWT), Docker escape
