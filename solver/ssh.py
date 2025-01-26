from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

class SSHConnection:
	"""
	A class to represent an SSH connection and perform operations over it.
	Attributes
	----------
	ip : str
		The IP address of the SSH server.
	port : int
		The port number of the SSH server.
	username : str
		The username to authenticate with the SSH server.
	password : str
		The password to authenticate with the SSH server.
	client : SSHClient
		The SSH client instance.
	scp : SCPClient
		The SCP client instance for file transfer.
	Methods
	-------
	__init__(ip, port, username, password):
		Initializes the SSH connection with the provided credentials.
	__del__():
		Destructor to ensure the connection is closed.
	close():
		Closes the SSH and SCP connections.
	exec(command: str) -> str:
		Executes a command on the SSH server and returns the output.
	download(file: str, dest: str = "."):
		Downloads a file from the SSH server to the local destination.
	"""

	def __init__(self, ip, port, username, password):
		self.ip = ip
		self.port = port
		self.username = username
		self.password = password
		self.client = SSHClient()
		self.client.set_missing_host_key_policy(AutoAddPolicy())
		try:
			self.client.connect(
				self.ip,
				port=self.port,
				username=self.username,
				password=self.password
			)
			self.scp = SCPClient(self.client.get_transport())
		except Exception as e:
			raise Exception(f"Failed to connect to {self.ip}:{self.port} as {self.username}")

	def __del__(self):
		self.close()

	def close(self):
		try:
			self.client.close()
			self.scp.close()
		except Exception as e:
			pass
		
	def exec(self, command: str) -> str:
		stdin, stdout, stderr = self.client.exec_command(command)
		error = stderr.read()
		if not error:
			return stdout.read().decode().strip()
		return "Error: " + error.decode().strip()
	
	def download(self, file: str, dest: str = "."):
		self.scp.get(file, dest)