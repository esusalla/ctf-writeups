- provided binary only has PIE security enabled
- running the binary reveals that it prints a "gift", which upon inspection turns out to be the base of the stack at that point
- it then asks for the length of your name and then allows you to enter your name
- it doesn't permit any name longer than 0x40, but this can be bypassed by entering a negative name length
- after sending a name, it checks that each byte of the name (with the exception of the last 8 bytes which it must permit for the address to be allowed) are greater than 0x30 ("0")
- this can be bypassed by using an alphanumeric shellcode
	- `XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V`

#### References:
	- https://www.exploit-db.com/exploits/35205
