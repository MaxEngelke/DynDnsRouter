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

INSTALL_DIR="$(realpath "${INSTALL_DIR}")"

#Read port for server socket
read -p "Enter server port(50110) : " PORT

if [ -z "$PORT" ]; then
    PORT=50110
fi

echo "Install to $INSTALL_DIR"

if [[ ! -d "$INSTALL_DIR" ]]; then
    mkdir $INSTALL_DIR
fi

#copy files
cp "$CURRENT_DIR/server/DynDnsServer.py" "$INSTALL_DIR"
cp -r "$CURRENT_DIR/dyndns_utils" "$INSTALL_DIR"

#install dependencies
echo "Install linux packages"
apt-get update
apt-get install socat
apt-get install pip

#incstall crypto for py
echo "Install python modules"
pip3 install cryptography
pip3 install psutils

#create keys
python "$INSTALL_DIR/dyndns_utils/crypto_utils.py" "$INSTALL_DIR"

#write default config file for client
CONFIG_FILE="$INSTALL_DIR/server.cfg"

echo "Creating server config file $CONFIG_FILE"

echo "server_port=$PORT
private_key=$INSTALL_DIR/private_key.pem" > $CONFIG_FILE

#create service
SCRIPT_FILE="$INSTALL_DIR/DynDnsServer.py"
chmod +x "$SCRIPT_FILE"

SERVER_USER="dyndnsserveruser"
#create user for service
useradd -r -s /bin/false $SERVER_USER
chown -R $SERVER_USER:$SERVER_USER "$INSTALL_DIR"

#unit file

echo "[Unit]
Description=DynDnsServer
After=syslog.target

[Service]
Type=simple
User=$SERVER_USER
Group=$SERVER_USER
WorkingDirectory=$INSTALL_DIR
ExecStart=$SCRIPT_FILE
SyslogIdentifier=DynDnsServer
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target" > "/etc/systemd/system/DynDnsServer.service"

systemctl enable DynDnsServer
systemctl start DynDnsServer

#try open port in firewalld

which firewall-cmd | grep -o firewall-cmd > /dev/null

if [ $? -eq 0 ]; then
    firewall-cmd --zone=public --add-port=$PORT/udp --permanent
    firewall-cmd --reload
fi

#create uninstall_server.sh

if [ -f uninstall_server.sh ]; then
    rm uninstall_server.sh
fi

echo "#!/bin/bash

systemctl stop DynDnsServer.service
systemctl disable DynDnsServer.service
rm -f /etc/systemd/system/DynDnsServer.service
rm -f /etc/systemd/system/DynDnsServer.service # and symlinks that might be related
rm -f /usr/lib/systemd/system/DynDnsServer.service
rm -f /usr/lib/systemd/system/DynDnsServer.service # and symlinks that might be related
systemctl daemon-reload
systemctl reset-failed

rm -rf $INSTALL_DIR

userdel $SERVER_USER

which firewall-cmd | grep -o firewall-cmd > /dev/null

if [ \$? -eq 0 ]; then
    firewall-cmd --zone=public --remove-port=$PORT/udp --permanent
    firewall-cmd --reload
fi

" >> "uninstall_server.sh"