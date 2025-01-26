from solver.config import *
from solver.utils import getflag
import subprocess

TMP_FILE = ".tmp"

def solve(connection):
	# Download the pcap file
	connection.download("/home/user/level02/level02.pcap", f"level02/resources")
	# Follow the stream of packets to find the flag password
	stream = subprocess.run(
		["tshark", "-r", f"level02/resources/level02.pcap", "-z", "follow,tcp,hex,0"], 
		capture_output=True, 
		check=True
	).stdout.decode("utf-8").split("\n")
	# Find the line with the prompt for password and strip what comes before it
	for i, l in enumerate(stream):
		if "Passw" in l:
			stream = stream[i+1:]
			break
	# Extract the password from the stream
	token = ""
	for l in stream:
		hex = l.split()[1] # The lines are in format "mem_addr hex ascii"
		if hex == "0d":
			break
		if hex == "7f": # Handle delete character
			token = token[:-1]
			continue
		ch = chr(int(hex, 16))
		token += ch
	flag = getflag("02", token)
	os.remove("level02/resources/level02.pcap")
	return token, flag