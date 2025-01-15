import subprocess
import os
from solver.utils import getflag

TEMP_FILE = ".tmp"
def solve(connection):
	flag_encrypted = connection.exec("getent passwd flag01 | cut -d ':' -f 2")
	with open(f"level01/resources/{TEMP_FILE}", "w") as f:
		f.write(flag_encrypted)
	# Run john the ripper on the temporary file and capture the output
	result = subprocess.run(
		["john", f"level01/resources/{TEMP_FILE}"], 
		capture_output=True,
		text=True,
		check=True
	)
	
	# Extract the cracked password from john's output
	john_show_result = subprocess.run(
		["john", "--show", f"level01/resources/{TEMP_FILE}"],
		capture_output=True,
		text=True,
		check=True
	).stdout.split()[0].split(":")[-1]
	# Return the cracked password
	flag = getflag("01", john_show_result)
	os.remove(f"level01/resources/{TEMP_FILE}")
	return john_show_result, flag