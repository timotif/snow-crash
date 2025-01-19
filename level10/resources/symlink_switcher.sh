#!/bin/bash
# Switching constantly a symlink between a file I own and the one I want 
while true
	do
		echo "MYFILE"
		ln -sf /tmp/myfile /tmp/token
		echo "TOKEN"
		ln -sf /home/user/level10/token /tmp/token
	done