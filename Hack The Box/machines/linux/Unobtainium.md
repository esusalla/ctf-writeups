# Summary

- Takeaways:
    - `package-lock.json` provides direct links to the package versions that are being run by the Node.js app, allowing you to inspect the exact sourcecode
    - after achieving foothold, upload static binaries (e.g., `nmap`, `gobuster`, etc.) for further recon on lateral movement opportunities (scan everything)
- User: creds included in package giving API access and leading to LFI and prototype pollution to gain permissions before injecting command into Node.js `exec` function for reverse shell
- Root: use private Docker registry to upload malicious image in order to move laterally before using Kubernetes privileges to spawn new container with root filesystem mounted in it

# Details

### User
- port scan reveals ports 22, 80, and 31337 are open as well as several ports (2379, 2380, 8443, 10250, 10256) associated with Kubernetes and ETCd
- website on port 80 has packages for different operating systems available for download (all of the checksums check out)
- possible to unpack any of the packages (chose the .deb package) to reveal the contents
- contains an Electron desktop application that allows you to make and retrieve notes as well as a todo list
- possible to unpack the included .asar file to reveal the source code driving the client-side application and directly inspect the web requests being made
	- https://github.com/electron/asar
	- can also packet sniff the application using WireShark and retrieve the web requests that way as well
- able to retrieve a username and password from the source files while also learning the format for requests
- the `/todo` endpoint takes a JSON with auth and filename parameters
- able to include local file from the same directory
- trying to retrieve `index.js` reveals the source code for the server, able to also pull `package.json` and `package-lock.json` to understand the app's dependencies
- server source code reveals an `/upload` endpoint (also found through fuzzing) and reveals an additional permission is needed to use it
- able to elevate permissions by using prototype pollution to bypass the `canUpload` object property check
	- https://github.com/Kirill89/prototype-pollution-explained
	- https://snyk.io/test/npm/lodash/4.17.4
- the `/upload` endpoint makes a call to the `upload` function within the `google-cloudstorage-commands` package, the source code of which can be retrieved using the link from `package-lock.json`
- the source code for the `upload` function shows that it's vulnerable to command injection as it calls the `exec` function from the `child_process` module without sanitizing the user input
- possible to send a malicious payload in the "filename" parameter of the upload request in order to spawn a reverse shell with a Python command and retrieve the user flag

### Root
- Kubernetes service token located at `/run/secrets/kubernetes.io/serviceaccount/token` has very limited privileges
	- container has `kubectl` binary removed, but can reupload and use
- uploading `nmap` and using it to scan for other pods / containers reveals there are 10 total containers, some of which have port 3000 open (potentially indicating the main server is running a reverse proxy on port 31337 that proxies requests to one of the six Node.js app containers)
	- `nmap -sT -p- 172.17.0.1-255`
- other interesting containers include one listening on port 5000 and another that has no open ports
- uploading `gobuster` and using it on the container with port 5000 open reveals it responds to the `/v2/` endpoint, indicating it's a private docker registry
- using the registry API, it's possible to list all images without any authentication using the `<host>:<ip>/v2/_catalog` endpoint
- the API reveals there are two containers, `node_server` and `dev-alpine`
- pulling down both container blobs and unpacking them doesn’t reveal any interesting files
	- download the blobs using the `<host>:<ip>/v2/<image>/blobs/<blob_hash>` endpoint and save them with the `.tar.gz` file extension before opening
	- https://notsosecure.com/anatomy-of-a-hack-docker-registry/
- possible to use SSH to set up remote port forwarding that would all direct access to the docker registry in the other container
	- after creating the `portforward` local user, creating SSH keys, and uploading the private key to the internal server we have access to, `ssh -i pf_ed25519 -R 10.10.14.114:5000:172.17.0.2:5000 portforward@10.10.14.114 -p 9998`
	- command forwards requests to the local port 5000 to the remote docker registry
	- https://linuxize.com/post/how-to-setup-ssh-tunneling/
- able to pull down the full `dev-alpine` image, run it with `docker run -it localhost:5000/dev-alpine:latest /bin/sh`, make internal changes (set up reverse shell script), then commit those changes with `docker commit <hash> <tag>`, and then use the newly commited image as the base for a Dockerfile that runs the reverse shell script as its final `CMD` parameter
- can then push the malicious image and wait for the reverse shell to be spawned
	- https://gabrieltanner.org/blog/docker-registry
- once we have access to the server running the Docker registry, we can again upload `kubectl` and check to see that the token on this machine has much high privileges
	- possible to save down the token and use the Kubernetes API locally to run commands, `wscat -n -H "Authorization: Bearer $KTOKEN" -c "https://unobtainium.htb:8443/api/v1/namespaces/kube-system/pods/backup-pod/exec?command=/root/rshell.sh&stdin=true&stderr=true&stdout=true"`
	- can trigger the reverse shell directly this way, but have to use `wscat` as `curl` does not support upgrading to a WebSocket
- possible to create a malicious pod that mounts the host machines root filesystem within itself and then `exec` into it for full access
	- `kubectl apply -f exploit-pod.yaml`
	- `kubectl exec -it <pod_name> -- chroot /host bash`
	- https://github.com/BishopFox/badPods
	- https://labs.bishopfox.com/tech-blog/bad-pods-kubernetes-pod-privilege-escalation


#### Tags: LFI, prototype pollution, Node.js command injection, Kubernetes escape
