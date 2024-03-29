# setDNS
> Small CLI utility to chage DNS settings on macOS

CLI utility to quickly chage DNS server settings on macOS. The `-d / --default`
sets the servers to [CloudFlare][cloudflare_article] DNS servers.

## Installation

macOS:

Clone the repository and run:

```sh
git clone https://github.com/polyrand/setDNS.git
chmod +x setdns.py
./setdns.py
```

## Usage example

* `./setdns.py -r` = Remove current DNS settings.
* `./setdns.py -f` = Flush DNS cache *(requires password)*.
* `./setdns.py -r -f` = Remove current DNS settings and flush the cache *(requires password)*.
* `./setdns.py -d` = Set servers to [cloudflare][cloudflare_article] DNS servers
* `./setdns.py -c` = Check current DNS server settings.

## Meta

[https://github.com/polyrand/](https://github.com/polyrand/)

[cloudflare_article]: https://blog.cloudflare.com/announcing-1111/
