# 2 of Spades (443)
- nmap scan reveals a `/.git` endpoing
- possible to pull files from the git directory, `dumper.sh` script helps
- one of the changes in the git log reveals the URL of the flag

# 9 of Diamonds (8080)
- website uses a cookie named `admin`
- possible to set the value to 1 and log in to retrieve the flag

# 4 of Diamonds (10010)
- post request to backend for registration uses array syntax, e.g., `account[password]=pass`
- possible to make a new account an admin by adding `account[role]=admin`

# 5 of Diamonds (11111)
- SQL injection on the login form allows you to login as admin with `' or 1=1--`

# 2 of Clubs (20000, 20001)
- provide with a game client that communicates with a server on the Ubuntu box
- game requires you to click targets that appear on the screen in a certain amount of time
- can sniff the packets between them to detect when the server send a new target
- once a target is detected, its location can be extracted and used to construct a response packet to destroy the target

# Black Joker (20001, 20001)
- hard version of the above game client
- communication between client and server now uses TLV encoding rather than plaintext
- can again sniff the communication between them and analyze the messages
- possible to determine which bytes correspond to the targets location and use them to construct a response packet

# Ace of Hearts (20011)
- website hosts photo galleries for various users, one of which is private
- also tells you that others can be found by searching directly for them
- able to enter retrieve the admin page through the SSRF functionality
- admin page allows you to set the private profile to public so the flag can be retrieved

# Jack of Hearts (20022)
- cookie for website is a double base64-encode serialized PHP object
- contains field for profile image path that is returned to you when logged in
- can replace the field with `/flag.png` to retrieve the flag

# 9 of Spades (20055)
- upload .htaccess file that allows you to execute PHP with custom extension
- use custom extension to bypass blacklist and achieve code execution

# 8 of Clubs (20123)
- trying to SSH in sends back a message that the user and password are both `root`
- logining in gives you a Python script to encrypt a file along with the encrypted file
- uses Fernet encryption and seeds random with a constant value
- possible to generate the key and decode the file to retrieve the flag

# Ace of Diamonds (35000)
- given a PCAP file and told it contains traffic that exfiltrates data
- PCAP contains some SMB traffic
- looking through traffic shows the data portion of a lot of requests contain an additional printable byte before them
- SMB packet contains a padding portion that is being used to exfiltrate data
- possible to reassemble the URL for the flag by putting together the bytes from the padding
