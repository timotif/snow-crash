#!/bin/bash

# Calling the program over and over
if [ -z $1 ]
then
	echo "Usage: $0 <host>"
	exit 1
fi
while true
	do
		/home/user/level10/level10 /tmp/token $1
	done