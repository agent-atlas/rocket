$ORIGIN freshnet.io.
@	3600 IN	SOA ns.freshnet.io. root.freshnet.io. (
				2018070500 ; serial
				7200       ; refresh in seconds (2 hours is 7200)
				3600       ; retry (1 hour)
				1209600    ; expire (2 weeks)
				3600       ; minimum (1 hour)
				)

	3600 IN NS ns.freshnet.io.

ns IN A 10.8.1.10
chat  IN A 10.8.1.3
wireguard IN A 10.8.1.2