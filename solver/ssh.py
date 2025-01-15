from paramiko import SSHClient, AutoAddPolicy

class SSHConnection:
	def __init__(self, ip, port, username, password):
		self.ip = ip
		self.port = port
		self.username = username
		self.password = password
		self.client = SSHClient()
		self.client.set_missing_host_key_policy(AutoAddPolicy())
		self.client.connect(
			self.ip,
			port=self.port,
			username=self.username,
			password=self.password
		)

	def __del__(self):
		self.close()

	def close(self):
		self.client.close()

	def exec(self, command: str) -> str:
		stdin, stdout, stderr = self.client.exec_command(command)
		error = stderr.read()
		if not error:
			return stdout.read().decode().strip()
		return "Error: " + error.decode().strip()