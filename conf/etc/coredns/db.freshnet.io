$TTL    1M
$ORIGIN freshnet.io.

freshnet.io.		    IN	SOA	sns.dns.icann.org. noc.dns.icann.org. 2015082541 7200 3600 1209600 3600
freshnet.io.		    IN	NS	b.iana-servers.net.
freshnet.io.		    IN	NS	a.iana-servers.net.
freshnet.io.		    IN	A	127.0.0.1

test.freshnet.io.	    IN	A	10.8.1.10

text.freshnet.io.	    IN	TXT	"This is a test text record"
chat               IN      A       10.8.1.3
vpn                  IN      A       10.8.1.2