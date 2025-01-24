from .ssh import SSHConnection
from .config import IP, PORT 
from paramiko import AuthenticationException

def extract_flag(response):
	if "Here is your token" in response:
		return response.split(':')[-1].strip()
	return None

def getflag(level, password) -> str | None:
	"""Connects as 'flag{level} and retrieves the flag from the server.
	If the flag is not found, returns None."""
	connection = SSHConnection(
		IP,
		PORT,
		f"flag{level}",
		password
	)
	response = connection.exec("getflag")
	return extract_flag(response)

def caesar_cipher(text: str, shift: int) -> str:
	if shift < 0:
		shift = 26 + shift
	shift = shift % 26
	return "".join(
		chr((ord(c) - 97 + shift) % 26 + 97)
		if c.islower() else c
		for c in text
	)