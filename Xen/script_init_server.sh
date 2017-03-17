#!/bin/sh

#Création du .bashrc
echo "Creation du .bashrc"
echo "alias ls='ls --color=auto'" >> .bashrc
echo "alias ll='ls --color=auto -lh'" >> .bashrc
echo "alias la='ls --color=auto -lAh'" >> .bashrc
cat .bashrc

#Création du .vimrc
echo "\nCreation du .vimrc"
echo "set background=dark" > .vimrc
echo "syntax on" >> .vimrc
echo "set number" >> .vimrc
echo "set smartindent" >> .vimrc
echo "set showmode" >> .vimrc
echo "set ruler" >> .vimrc
echo "set showcmd" >> .vimrc
echo "set mouse=a" >> .vimrc
cat .vimrc

#Téléchargement de l'image XEN
apt-get install gpm xen-linux-system xen-docs-4.1

#Modification du Boot
mv /etc/grub.d/06_OVHkernel /etc/grub.d/07_OVHkernel
mv /etc/grub.d/20_linux_xen /etc/grub.d/06_linux_xen

# Update du grub
update-grub

#Reboot
reboot