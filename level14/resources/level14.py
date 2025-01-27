from solver.utils import getflag

def solve(connection):
	connection.upload("level14/resources/instructions.gdb", "/tmp/instructions.gdb")
	output = connection.exec("gdb -batch -q -x /tmp/instructions.gdb getflag")
	token = output.split("\n")[-2].split()[-1]
	connection.exec("rm -f /tmp/instructions.gdb")
	return token, getflag("14", token)