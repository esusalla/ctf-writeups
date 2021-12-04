# Summary
- User: use the backdoor inserted into the PHP/8.1.0-dev codebase in order to write the already present `/home/james/id_rsa.pub` into an `authorized_keys` file
- Root: able to run `/usr/bin/knife` with `sudo`, meaning you can run arbitrary Ruby commands as `root` with `knife exec`

# Details
### User
- port scan reveals ports 22 and 80 are open
- website enumeration doesn't turn up much, but trying to navigate to a `.php` file sends back a response with the `X-Powered-By: PHP/8.1.0-dev` header
- this version of PHP had an issue with a compromised Git server and a backdoor was inserted into the codebase
- the app will look for requests with a `User-Agentt` (with two t's) header that starts with `zerodium` and then execute whatever follows in PHP (`User-Agentt: zerodiumsystem("ls -al");`)
- https://nakedsecurity.sophos.com/2021/03/30/php-web-language-narrowly-avoids-dangerous-supply-chain-attack/
- this allows you to read the `id_rsa` and `id_rsa.pub` files in `/home/james/.ssh` and additionally write the `id_rsa.pub` into `/home/james/.ssh/authorized_keys` which permits SSHing in

### Root
- `james` user is able to run `sudo /usr/bin/knife`
- `knife` is a binary that's part of the `Chef Infra` product which bills itself as a "complete automation solution for both infrastructure and applications"
- `knife` binary has an `exec` command that allows you to run Ruby scripts or commands (`sudo /usr/bin/knife exec -E 'system("/bin/bash")'`)
- https://docs.chef.io/workstation/knife_exec/

#### Tags: PHP backdoor
