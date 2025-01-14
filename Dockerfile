FROM kalilinux/kali-rolling

RUN apt update && apt upgrade -y

RUN apt install -y \
	john

CMD ["/bin/bash"]