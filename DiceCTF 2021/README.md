# Pwn

### BabyRop: dice{so_let's_just_pretend_rop_between_you_and_me_was_never_meant_b1b585695bdd0bcf2d144b4b}
- provided with a binary that lacks canary protections
- possible to leak addresses and fingerprint libc
- after leaking addresses, you can use ret2csu in order to open a shell
- https://bananamafia.dev/post/x64-rop-redpwn/


# Web

### Missing Flavortext: dice{sq1i_d03sn7_3v3n_3x1s7_4nym0r3}
- index.js uses "app.use(bodyParser.urlencoded({ extended: true }))"
- makes it possible to send arrays and other data types that can bypass the single quote filter and perform a fragmented SQL injection
- doubling up a single quote escapes it, so entire username string becomes "', '' AND password = '"
- query ends up becoming "SELECT id FROM users WHERE username = ', '' AND password = ' OR 1=1-- '" allowing flag retrieval
