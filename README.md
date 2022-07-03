DynDnsService

This project is for people having a homeserver behind an ipv6 isp connection.
I use an external v-server for handling connections via this project and reconnect them to my homeserver.
Every client on my homeserver, whether a vpn container or nextcloud or whatever, has a client service running to inform the
server about changing ip addresses.
When the server is informed, it creates a new socat process with the transmitted parameters.