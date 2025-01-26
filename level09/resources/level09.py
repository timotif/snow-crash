import os
from solver.utils import getflag

TMP_FILE = "level09/resources/.tmp"

def decrypt(data: bin):
	token = "".join([chr(c - i) for i, c in enumerate(data) if c != 0x0a])
	return token

def solve(connection):
	connection.download("/home/user/level09/token", TMP_FILE)
	with open(TMP_FILE, "rb") as f:
		token = decrypt(f.read())
	flag = getflag('09', token)
	os.remove(TMP_FILE)
	return token, flag