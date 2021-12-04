 Summary
- Takeaways:
    - take name of box into bigger consideration, especially when hitting dead ends
    - can run `strings` directly on `/dev` files to view recently deleted data that has not yet been written over
- User: recognize the machine is a Raspberry Pi and log in with default credentials (hint at Mirai botnet using default credentials for its exploits)
- Root: user can directly escalate to root through `sudo` privileges, then there's a short scavenger hunt for the true root flag which can be found by running `strings` on `/dev/sdb` (before file was deleted it was on the USB drive that is currently mounted at `/dev/sdb`)

# Details
### User: ff837707441b257a20e32199d7c8838d
- Nmap scan reveals port 22, 53, 80, 1641, 32400, and 32469 are open
- the target functions as a Pi-hole (DNS blackhole for blocking advertisements and other content) and also hosting a Plex server
- various enumeration techniques and attempting to bruteforce the whitelist function of the Pi-hole homepage yielded nothing, the Pi-hole admin page at `/admin` was also a dead end
- the clue was the name of the box hinting at the Mirai botnet, which used default credentials to take over IoT devices
- the default Raspberry Pi credentials are `username: pi` and `password: raspberry`, which can be used to SSH in to the target

### Root: 3d3e483143ff12ec505d026fa13e020b
- the `pi` user has all `sudo` privileges and can directly escalate to root
- the `root.txt` flag is replaced with a message that the original `root.txt` has been lost and was previously on a flashdrive
- inspecting the `/media` mountpoint reveals the `usbdrive` directory with a file named `damnit.txt` in it that says the files on the USB were accidentally deleted
- searching the USB mountpoint (`/dev/sdb`) with `debugfs` came up with nothing, but running `strings` directly on `/dev/sdb` reveals the root flag left over from the deleted file
