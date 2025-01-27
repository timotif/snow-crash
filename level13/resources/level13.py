def solve(connection):
	connection.upload("level13/resources/instructions.gdb", "/tmp/instructions.gdb")
	output = connection.exec("gdb -batch -q -x /tmp/instructions.gdb ./level13")
	flag = output.split("\n")[-1].split()[-1].strip("\"")
	connection.exec(f"rm /tmp/instructions.gdb")
	return "", flag