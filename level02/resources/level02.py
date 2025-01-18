from solver.config import *
import subprocess

TMP_FILE = ".tmp"

def solve(connection):
	print(connection.username)
	stdin, stdout, stderr = connection.download("/home/user/level02/level02.pcap", f"level02/resources")
	stdin.write(connection.password + "\n")
	return "", ""