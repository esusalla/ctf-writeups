# Pwn

### C'mon See My Vulns: CTF-BR{f4ke_fl4g_f0r_t3st1ng!}
- provided with the source code for a PHP backend that uses a custom `csvparser.so` extension
- webpage takes in CSV and parses it into PHP array
- can also pass commands between double brackets which get ran with `eval`
- config disables all execution functions and sets the "open_basedir" path, but there's an unintended solution that allows you to bypass both of these settings so that full RCE can be achieved within the PHP `eval`
- possible to use Chankro from Tarlogic to achieve RCE
- https://github.com/TarlogicSecurity/Chankro
- https://www.tarlogic.com/en/blog/how-to-bypass-disable_functions-and-open_basedir/
- https://snix0.com/posts/pwn2win-cmon-see-my-vulns/


# Web

### Illusion: CTF-BR{d0nt_miX_pr0totyPe_pol1ution_w1th_a_t3mplat3_3ng1nE!}
- provided with source code for Node.js app that uses the EJS templating engine along with a JSON patch library
- investigating the GitHub repository for `fast-json-patch` reveals a recent pull request that is meant to fix a prototype pollution vulnerability
    - currently protects against prototype pollution that uses `__proto__`, but not those that use `constructor/prototype`
    - https://github.com/Starcounter-Jack/JSON-Patch/pull/262
- searching for RCE exploits within the EJS templating engine returns a a GitHub issues thread that discusses how the `outputFunctionName` option within EJS can be used to achieve RCE
    - https://github.com/mde/ejs/issues/451
- possible to use the prototype pollution vulnerability to set the value of `outputFunctionName` that is referenced within EJS
- if set, the string in this property is executed, allowing you to achieve RCE and execute the `/readflag` binary through `process.mainModule.require('child_process').execSync('/readflag').toString()`
- https://blog.p6.is/Real-World-JS-1/

### Ruthless Monster
- provided with the source code for a PHP backend that allows you to upload a PDF (checks the magic bytes) and then runs `exiftool` on it
- Dockerfile reveals exiftool version 12.23 is used
- the exiftool version history page contains a note in version 12.24 that mentions a "security vulnerability in DjVu reader"
    - https://exiftool.org/history.html
- searching for this brings up a Medium article detailing the exploit
    - possible to create a malicious Djvu file with `djVumake` and then embed it into an image file using a writable tag
    - can then overwrite the tag ID bytes so that `exiftool` thinks it's parsing a HasselbladExif tag (0xc51b) which gets passed to the vulnerable DjVu parser and allows for RCE
    - https://amalmurali47.medium.com/an-image-speaks-a-thousand-rces-the-tale-of-reversing-an-exiftool-cve-585f4f040850
