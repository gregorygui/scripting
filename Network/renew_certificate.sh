#!/bin/bash

echo "déplacement dans le répertoire des certificats perso..."
cd /etc/ssl/certs/Cert_Perso
pwd
rm /etc/ssl/certs/Cert_Perso/*

echo "génération du certificat de l'authorité..."
openssl genrsa -des3 -out ca.key 4096
openssl req -x509 -new -sha512 -nodes -key ca.key -days 365 -out ca.pem

echo "génération du certificat serveur..."
openssl genrsa -out server.key 4096
openssl req -new -sha512 -key server.key -out server.csr
openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha512

mv /etc/xensource/xapi-ssl.pem /etc/xensource/xapi-ssl.pem_origin

cat server.crt server.key > server.pem 
chmod 600 server.* ca.*

install -m 0400 server.pem /etc/xensource/xapi-ssl.pem

echo "restart xapissl..."
/etc/init.d/xapissl restart
