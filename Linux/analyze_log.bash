#!/bin/bash

# Grep vpn logs
cat /var/log/daemon.log*|grep -i -A1 "initiated"

# Grep ssh logins
cat /var/log/auth.log*|grep -i -B1 "(sshd:session): session opened"

# Grep sudo logins
cat /var/log/auth.log*|grep -i -B1 "(sudo:session): session opened"

# Grep bad access lighthttpd
sudo cat /var/log/lighttpd/access.log*|grep -iv -A1 "|200|\||304|"

# Get new iptables rules
cat auth.log|grep -i "iptables -A"|uniq -c

# Get ssh failed login
awk '/sshd\[[0-9]+\]\: Failed password for root from/ {print $11}' auth.log|uniq -c|wc -l

# Get ssh root successfull login
grep -E "sshd\[[0-9]+\]\: Accepted password for root from" auth.log|awk '{ print $11 }'|uniq -c|wc -l

# Get IP src web access
awk '{ print $12 }' apache2/www-access.log|uniq -c

# Get successfull login from a specific IP
grep "XX.XX.XX.XX" auth.log|grep "Accepted password for"

# Get successfull VPN connexions
find /var/log/openvpn/ -type f -exec grep -a " MULTI: Learn: " {} \;|awk '{ print $1,$2,$3,$4,$10,$12}'

# Get successfull VPN connexions and submit public ones to greynoise
find /var/log/openvpn/ -type f -exec grep -a " MULTI: Learn: " {} \;|awk '{ print $12 }'|awk -F '/' '{print $2}'|awk -F ':' '{ print $1 }'|sed -ne /./p|sort|uniq|grep -v "^1[79][0-9]"|while read ip; do curl -XGET "https://api.greynoise.io/v3/community/$ip" >> res_vpn.txt; echo "" >> res_vpn.txt ; done

# Get all IP from logs minus private ones
sudo find /var/log/ -type f -exec grep -a -o -E "([0-9]{1,3}\.){3}[0-9]{1,3}" {} \;|sort|uniq -c|grep -v -E "((1(7|9)2\.)|10\.|127\.|2(4|5)[0-9])"
