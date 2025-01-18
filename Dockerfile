FROM kalilinux/kali-rolling

RUN apt update && apt upgrade -y
# net-tools
# ssh
# iputils-ping
# xxd

# pip install paramiko \
#				scp

RUN apt install -y \
	ssh \
	john

CMD ["/bin/bash"]