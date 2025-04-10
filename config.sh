#!/bin/bash

### COLORS ###
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
WHITE='\033[0;37m'
RESET='\033[0m'

clear
echo -e "${RED}"
echo -e "	   _____                      _____               _"
echo -e "	  / ____|                    / ____|             | |    "
echo -e "	 | (___  _ __   _____      _| |     _ __ __ _ ___| |__  "
echo -e "	  \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _\` / __| '_ \ "
echo -e "	  ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |"
echo -e "	 |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|"
echo 
echo -e "${GREEN}Welcome to the Snow Crash environment configuration script!${RESET}\n"
echo -e "${YELLOW}This script will install all the necessary tools and dependencies for the Snow Crash project.${RESET}\n"
echo -e "${YELLOW}1. Boot ${BLUE}SnowCrash.iso${YELLOW} virtual machine with your favorite emulator.${RESET}"
read -p "Press Enter when ready..."
echo -ne "${YELLOW}2. What's the IP address that the virtual machine is showing?${RESET}\n"
read -e IP
sed -i "s/^IP = .*/IP = $IP/" Makefile && echo -e "${GREEN}IP address updated in Makefile${RESET}"
echo -ne "${YELLOW}3. What's the port the virtual machine is listening to? ${BLUE}(Default 4242)${RESET}\n"
read -e PORT
if [ -z "$PORT" ]; then
  PORT=4242
fi
sed -i "s/^PORT = .*/PORT = $PORT/" Makefile && echo -e "${GREEN}SSH port updated in Makefile${RESET}"
echo -e "\n${GREEN}That should do it! Configuration complete.${RESET}\n"