#!/bin/bash
#Si tu lances ce script c'est que tu viens juste de résintaller ton serveur
#Changement du mot de passe root
#http://wiki.xenproject.org/wiki/Network_Configuration_Examples_(Xen_4.1%2B)
passwd root

#Installer xen 
apt-get install xen-linux-system 

#Changer l'ordre de boot
mv /etc/grub.d/06_OVHkernel /etc/grub.d/07_OVH
mv /etc/grub.d/20_linux_xen /etc/grub.d/06_linux_xen
update-grub

#Reboot
reboot

#A installer après reboot
apt-get install xen-utils xen-tools xenwatch xcp-xe xcp-xapi

#A mettre dans /etc/network/interfaces
auto eth0
iface eth0 inet manual

auto xenbr0
iface xenbr0 inet static
	bridge_ports eth0
	address 151.80.44.35
	gateway 151.80.44.254
	netmask 255.255.255.0
	broadcast 151.80.44.255

#A mettre dans /etc/sysctl.conf
net.bridge.bridge-nf-call-ip6tables = 0
net.bridge.bridge-nf-call-iptables = 0
net.bridge.bridge-nf-call-arptables = 0
net.ipv4.ip_forward = 1
net.ipv4.conf.eth0.proxy_arp = 1

#Définition de xapi (pour utiliser xen orchestra plus tard)
echo 'TOOLSTACK="xapi"' > /etc/default/xen

# Pour exécuter les commandes suivantes
# Il est nécessaire d'avoir obtenu les
# Informations grâce aux trois commandes
# ci-dessous
df -h
cat /proc/partitions
ll /dev/disk/by-id
xe host-list

xe sr-create content-type=user device-config:device=/dev/disk/by-id/<scsi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx> host-uuid=<host-uuid> name-label="Local Storage" shared=false type=<ext|lvm>

#Création du pool
xe vm-import filename="" sr-uuid=