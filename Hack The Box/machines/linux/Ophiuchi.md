 Summary
- Takeaways:
	- don’t always trust error messages
	- pay attention to relative paths when things seem to not be working
- User: insecure YAML deserialization leading to RCE, creds in config file
- Root: WASM manipulation and relative path shadowing

# Details
### User
- ports 22 and 8080 are open with a website running on 8080 that asks for a YAML file to parse
- sending it anything returns an error that there has been a security issue so the service is down
- attempting to POST to the `/Servlet` endpoint where the parser is without supplying a `data` param causes the Java web app to try and read a null string which causes an error and returns the call stack
- call stack makes it possible to see that the vulnerable `yaml.load()` function is actually still being called with our input despite what the warning message side
- possible to construct a malicious .jar file that executes arbitrary commands when run, we then inject commands into the YAML file which create Java classes that request and execute the malicious .jar file
- successful execution of the malicious .jar grants shell access as `www-data`
- searching the app directory for anything interesting reveals creds for the `admin` user
- https://pulsesecurity.co.nz/advisories/Insecure-YAML-Deserialisation
- https://github.com/artsploit/yaml-payload

### Root
- `sudo -l` reveals `admin` can run `/usr/bin/go run /opt/wasm-functions/index.go`
- checking the source file, it looks like it attempts to load a file called `main.wasm` and then calls the function `info` exported from that file
- `main.wasm` is a relative filepath, allowing us to run our own `main.wasm` as long as it's in our current directory when executing the sudo command
- if the function returns `1` then `setup.sh` is executed in the same directory
- `setup.sh` is also a relative path, so we can execute anything we want once the WASM condition is met
- possible to use `wasm-objdump -d main.wasm` to better inspect what the function code does
- consists of just the `info` function which returns `0`
- possible to overwrite the byte that is returned with `1` so that the condition is satisfied when running
	- `printf '\x01' | dd of=main.wasm bs=1 seek=110 count=1 conv=notrunc`
- also possible to compile a WASM module that fulfills the requirements (exported function named "info" that returns 1)
		- compile wasm.c: `emcc --no-entry wasm.c -o main.wasm -s EXPORTED_FUNCTIONS='["_info"]'`
- running the sudo command again will execute `setup.sh` and launch the reverse shell
- https://github.com/WebAssembly/wabt (WebAssembly Binary Toolkit)

#### Tags: WASM
