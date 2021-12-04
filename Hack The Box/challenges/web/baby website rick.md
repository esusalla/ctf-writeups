- Takeaways:
	- if RCE through unpickling is not working for some reason, try using Python2 to pickle the objects
	- be sure to match the `protocol` parameter of `pickle.dumps` to what the original cookie appears to have used (`protocol` can range from 0 to 5)
- presented with a website that appears to be printing back a raw Python object
- inspecting the cookies reveals one named `plan_b` with a base64-encoded string for the value
- decoding the string reveals it to be a pickled Python object
- inspecting the disassembled pickle with `pickletools.dis(<unpickled>)` shows that it appears to be a pickled object of the form `{"serum": <anti_pickle_serum>}`
- this all points to a Python unpickling / deserialization vulnerability
- possible to construct a malicious `anti_pickle_serum` class that implements the special function `__reduce__` to achieve RCE
- after trying several payloads, it seems that we can't connect to any outside listeners and will have to use a blind method to retrieve the flag
- the only code execution functions that seem to work are those within the global namespace or within the `os` module (found out after it was possible to get execution with the `subprocess` module by using Python2, but unsure of why this is the case)
- unfortunately, `os.system` does not return standard output so we're unable to get the output of commands (hence the need for blind injection)
- possible to use `<cmd> && sleep 2` and then measure the response time (`res.elapses.total_seconds()`) to find which commands are successful
- can first use `os.listdir` to enumerate the filesystem and find the exact location of the flag before using the command `grep <flag> <path> && sleep 2` to recover the flag a character at a time
- found out after completing that it's possible to achieve easy execution of `subprocess.check_output` which will allow you to directly read the stdout of a command by using Python2 to pickle the malicious object
```python
class anti_pickle_serum:
    def __init__(self, cmd):
        self.cmd = cmd

    def __reduce__(self):
        # use to find exact name / location of flag
        #return os.listdir, ("/app",) 
        return os.system, (self.cmd,)
```
#### Flags: blind unpickling / deserialization
