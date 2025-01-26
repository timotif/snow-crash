FROM kalilinux/kali-rolling

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y && \
	apt install -y \
	python3-pip \
	python3-venv \
	ssh \
	john \
	tshark
# net-tools
# ssh
# iputils-ping
# xxd

# pip install paramiko \
#				scp

# Activating the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

RUN python3 -m venv /opt/venv && \
	pip install --upgrade pip && \
	pip install paramiko \
				scp

WORKDIR /snow-crash

CMD ["/bin/bash"]