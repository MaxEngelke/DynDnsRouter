#!/bin/bash

CURRENT_DIR="$(dirname "${BASH_SOURCE[0]}")"
CURRENT_DIR="$(realpath "${CURRENT_DIR}")"

#Get installation dir if provided as argument or ask for it.
#If nothing is provided use current dir.
if [ -z "$1" ]; then
        read -p "Enter install dir : " INSTALL_DIR

        if [ -z "$INSTALL_DIR" ]; then
            INSTALL_DIR=$CURRENT_DIR
        fi
    else
        INSTALL_DIR=$1
fi

echo "Install to $INSTALL_DIR"

if [[ ! -d "$INSTALL_DIR" ]]; then
    mkdir $INSTALL_DIR
fi

#copy files
cp "$CURRENT_DIR/client/DynDnsClientUpdate.py" "$INSTALL_DIR"
cp -r "$CURRENT_DIR/dyndns_utils" "$INSTALL_DIR"

#write default config file for client
CONFIG_FILE="$INSTALL_DIR/client.cfg"

read -p "Enter server ip : " SERVER_IP

read -p "Enter server port (50110) : " SERVER_PORT

if [ -z "$SERVER_PORT" ]; then
    SERVER_PORT=50110
fi

echo "Creating server config file $CONFIG_FILE"

echo "server_ip=$SERVER_IP
server_port=$SERVER_PORT
client=
tunnel_ports_tcp=
tunnel_ports_udp=
current_ip=
current_ip_version=ipv6
public_key=" > "$CONFIG_FILE"

#install dependencies
apt-get update
apt-get install pip

#incstall crypto for py
echo "Install python module cryptography"
pip3 install cryptography

#add user

CLIENT_USER="dyndnsclientuser"
#create user for service
useradd -r -s /bin/false $CLIENT_USER
chown -R $CLIENT_USER:$CLIENT_USER "$INSTALL_DIR"

#install cron job

COMMAND="python3 $INSTALL_DIR/DynDnsClientUpdate.py"

grep -qi "$CLIENT_USER" /etc/cron.allow

if [ $? != 0 ]; then
    echo "$CLIENT_USER" >> /etc/cron.allow
fi

(crontab -u $CLIENT_USER -l ; echo "* * * * * $COMMAND") | crontab -u $CLIENT_USER -

#create uninstall_client.sh

if [ -f uninstall_client.sh ]; then
    rm uninstall_client.sh
fi

echo "#!/bin/bash

rm -rf $INSTALL_DIR

crontab -u $CLIENT_USER -l | grep -v '$COMMAND'  | crontab -u $CLIENT_USER -

userdel $CLIENT_USER

" >> "uninstall_client.sh"