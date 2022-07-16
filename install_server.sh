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
cp "$CURRENT_DIR/server/DynDnsServer.py" "$INSTALL_DIR"
cp -r "$CURRENT_DIR/dyndns_utils" "$INSTALL_DIR"

#install socat
apt-get install socat

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

#add daemon