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

echo "Creating server config file $CONFIG_FILE"

echo "server_ip=
server_port=
client=
tunnel_ports_tcp=
tunnel_ports_udp=
current_ip=
public_key=" > "$CONFIG_FILE"

#incstall crypto for py
echo "Install python module cryptography"
pip3 install cryptography

#install cron job