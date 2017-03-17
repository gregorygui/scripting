#!/bin/sh

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade
sudo apt-get --purge autoremove

sudo apt-get install htop vim python3-pip tree virtualbox-guest-additions-iso

echo "set background=dark
syntax on
set number
set autoindent
set smartindent
set showmode
set ruler
set showcmd
" > ~/.vimrc

echo"
alias ll='ls -lh'
alias la ='ls lha'
alias python='python3'
alias pip='pip3'
" >> ~/.bashrc