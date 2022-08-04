DynDnsService

This project is for people having a homeserver behind an ipv6 isp connection.
I use an external v-server for handling connections via this project and forward them to my homeserver.
Every client on my homeserver, whether a vpn container or nextcloud or whatever, has a client service running to inform the
server about changing ip addresses.
When the server is informed, it creates a new socat process with the transmitted parameters.

On the server you just need to install "install_server.sh" and may open the firewall ports.
A public and private key pair are generated.


On the client side you need to install "install_client.sh" and get the public key from the server.

server_port=                    #port yoiu choose on the serverside
client=                         #client name
tunnel_ports_tcp=               #tcp ports to open. (e.g. 80-443 spawns socat for server port 80 to client port 443. Add more with ";"
tunnel_ports_udp=               #udo ports to open. same as above
current_ip=                     #auto filled
current_ip_version=ipv6         #can be ipv4 for or ivp6 deppending on your global ip address from isp
public_key=public_key.pem       #path to public key