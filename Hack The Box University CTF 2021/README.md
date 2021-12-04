# Pwn

### Robot Factory: HTB{th3_r0b0t5_4r3_0utt4_c0ntr0l!}
- provided with a binary that has canary protections but no PIE
- incorrect call to `printf` leaks value that can be used to calculate libc base
- function called in pthread allows for stack overflow
- due to the fact that the Thread Control Block in threads is placed above the local thread stack in memory, it's possible to overflow both the local canary as well as the reference canary help in the TCB so that they both still match
- can use the above to overwrite the return address with a one gadget address while also passing the canary check


# Web

### Slippy: HTB{i_slipped_my_way_to_rce}
- website allows you to upload a gzipped tar file which it opens and stores on the server
- possible to use `../` within the path when creating the gzipped tar so that when it's unpacked it overwrites files on the server at known locations
- can then use our uploaded files to achieve command execution

### SteamCoin: HTB{w3_d0_4_l1ttl3_c0uch_d0wnl04d1ng}
- provided with the sourcecode for a Node.js application
- app allows you to register, login, and upload files
- uses JWTs for authorization with JKU and KID in header
- possible to upload a forged JWKS file and point the JKU header value to it so that your forged JWT validates
- can use to the above to impersonate the admin
- still need to be able to reach the `/api/test-ui` endpoint which is denied by HAProxy if the request isn't coming from the localhost
- need to use HTTP request smuggling to pass HAProxy's ACL rule (HAProxy views it as only a single request while the backend application server parses it as two separate)
- with admin privileges and access to `/api/test-ui`, it's possible to make the server bot visit a local webpage
- can upload a second file with an XSS payload that causes the server bot to make a request to the local CouchDB server and exfiltrate the flag back to you


# Cloud

### SteamCloud
- given the IP address of a Kubernetes cluster
- nmap scan reveals the open ports
- misconfigured Kublet API on port 10250 allows you to execute commands on containers and retrieve service tokens
- one of the service tokens has privileges that allows it to create new pods
- possible to create a malicious pod that mounts the host server's main drive which contains the flag


# Misc

### Insane Bolt: HTB{w1th_4ll_th353_b0lt5_4nd_g3m5_1ll_cr4ft_th3_b35t_t00ls}
- service is hosted that sends you a level where you need to navigate through a path and collect gems while avoiding obstacles
- need to solve the challenge 500 times to retrieve the flag
- possible to convert the gameboard into a graph and then use BFS to get the best path to the exit
- can then convert the path into the needed format and send it back to solve each level
