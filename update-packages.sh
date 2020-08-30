#!/bin/bash
#update.sh updates archlinux packages that arent managed with pacman

update_package()
{
	echo "updating package: $1"
	curl -O -L "https://aur.archlinux.org/cgit/aur.git/snapshot/$1"
 	tar -xvzf "$1"
 	cd `echo "$1" | rev | cut -c8- | rev`
 	pwd
 	if [[ $? -eq 0 ]]; then
 		pwd
 		makepkg -si --noconfirm
 		cd /home/holden/Downloads/packages
 	fi	
}

mark_package()
{
	mv -v "$1" "$1.no"
}

unmark_package()
{
	NEW_NAME=`echo "$1" | rev | cut -c4- | rev`
	mv -v "$1" "$NEW_NAME"
}

reset()
{
	#ls | grep "\..z$"
	for package in $( ls | grep "\.no$" ); do
		unmark_package $package
	done
}

check()
{
	ls | grep "\.no$"
	ls | grep "\..z$"
}

normal()
{
	#ls | grep "\..z$"
	for package in $( ls | grep "\..z$" ); do
		echo "do you want to update this package?(y/n/s):     $package"
		read input
		case $input in
			"y")
				update_package $package
			;;
			"s")
			;;
			*)
				mark_package $package
			;;
		esac
	 done
}

cd /home/holden/Downloads/packages
case $1 in
	"reset")
		reset
	;;
	"normal")
		normal
	;;
	"check")
		check
	;;
	*)
		echo "do reset to reset marked packages, normal to run normal mode"
	;;
esac
cd -