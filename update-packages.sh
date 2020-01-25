#!/bin/bash
#update.sh updates archlinux packages that arent managed with pacman

cd /home/holden/Downloads
for package in $( ls | grep "\..z$" ); do
	curl -O -L "https://aur.archlinux.org/cgit/aur.git/snapshot/${package}"
	cd `echo "${package}" | rev | cut -c8- | rev`
	if [[ $? -eq 0 ]]; then
		pwd
		makepkg -si --noconfirm
		cd /home/holden/Downloads
	fi	
done
