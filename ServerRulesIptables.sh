echo "Flush des regles actuelles..."
iptables -F
iptables -t nat -F

echo "Activation du routage Kernel..."
echo 1 > /proc/sys/net/ipv4/ip_forward

echo "Accept ping..."
iptables -A INPUT -i xenbr1 -p icmp -j ACCEPT

echo "Accept SSH, Web, GitLab, RDP Kali..."
iptables -A INPUT -i xenbr1 -p tcp -m tcp --dport 22 -j ACCEPT
iptables -A INPUT -i xenbr1 -p tcp -m tcp --dport 80 -j ACCEPT
iptables -A INPUT -i xenbr1 -p tcp -m tcp --dport 443 -j ACCEPT
iptables -A INPUT -i xenbr1 -p tcp -m tcp --dport 5555 -j ACCEPT
iptables -A INPUT -i xenbr1 -p tcp -m tcp --dport 5556 -j ACCEPT
iptables -A INPUT -i xenbr1 -p tcp -m tcp --dport 8080 -j ACCEPT

echo "Acces internet VM..."
iptables -t nat -A POSTROUTING --out-interface xenbr1 -j MASQUERADE

echo "Redirection GitLab..."
iptables -t nat -A PREROUTING -i xenbr1 -p tcp -m tcp --dport 8080 -j DNAT --to-destination 169.254.0.36:80

echo "Redirection RDP Kali..."
iptables -t nat -A PREROUTING -i xenbr1 -p tcp -m tcp --dport 5555 -j DNAT --to-destination 169.254.0.37:3389

echo "Redirection RDP NeXpose..."
iptables -t nat -A PREROUTING -i xenbr1 -p tcp -m tcp --dport 5556 -j DNAT --to-destination 169.254.0.38:3389

echo "Accepter les retours type DNS, yum..."
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

echo "Blocage du reste..."
iptables -A INPUT -i xenbr1 -p all -j REJECT

echo "Sauvegarde des regles..."
#service iptables save
