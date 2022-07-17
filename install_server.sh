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

echo "Install to $INSTALL_DIR"

if [[ ! -d "$INSTALL_DIR" ]]; then
    mkdir $INSTALL_DIR
fi

#copy files
cp "$CURRENT_DIR/server/DynDnsServer.py" "$INSTALL_DIR"
cp -r "$CURRENT_DIR/dyndns_utils" "$INSTALL_DIR"

#install dependencies
apt-get update
apt-get install socat
apt-get install pip

#incstall crypto for py
echo "Install python module cryptography"
pip3 install cryptography

#create keys
python "$INSTALL_DIR/dyndns_utils/crypto_utils.py" "$INSTALL_DIR"

#write default config file for client
CONFIG_FILE="$INSTALL_DIR/server.cfg"

echo "Creating server config file $CONFIG_FILE"

echo "server_port=
private_key=$INSTALL_DIR/private_key.pem" > $CONFIG_FILE

#create service
SCRIPT_FILE="$INSTALL_DIR/DynDnsServer.py"
chmod +x "$SCRIPT_FILE"

SERVER_USER="dyndnsserveruser"
#create user for service
useradd -r -s /bin/false $SERVER_USER
chown -R py $SERVER_USER:$SERVER_USER "$INSTALL_DIR"

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

