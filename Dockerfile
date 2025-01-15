FROM kalilinux/kali-rolling

RUN apt update && apt upgrade -y
# net-tools
# ssh
# iputils-ping

# pip install paramiko

RUN apt install -y \
	john

CMD ["/bin/bash"]