#!/bin/bash

# Grep vpn logs
cat /var/log/daemon.log*|grep -i -A1 "initiated"

# Grep ssh logins
cat /var/log/auth.log*|grep -i -B1 "(sshd:session): session opened"

# Grep sudo logins
cat /var/log/auth.log*|grep -i -B1 "(sudo:session): session opened"

# Grep bad access lighthttpd
sudo cat /var/log/lighttpd/access.log*|grep -iv -A1 "|200|\||304|"