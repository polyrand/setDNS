# setDNS
> Small CLI utility to chage DNS settings on macOS

One to two paragraph statement about your product and what it does.

![](header.png)

## Installation

macOS:

Clone the repository and run:

```sh
git clone https://github.com/rickaa/setDNS.git
chmod +x setdns.py
./setdns.py
```

## Usage example

./setdns.py -r = Remove current DNS settings.
./setdns.py -f = Flush DNS cache *(requires password)*.
./setdns.py -r -f = Remove current DNS settings and flush the cache *(requires password)*.
./setdns.py -d = Set servers to [cloudflare][cloudflare_article] DNS servers
./setdns.py -c = Check current DNS server settings.

## Meta

[https://github.com/rickaa/](https://github.com/rickaa/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


[cloudflare_article]: https://blog.cloudflare.com/announcing-1111/
