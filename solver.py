from solver.config import * 
from solver.ssh import SSHConnection
import json
import importlib
import os

flags = {}
prev = "00"

def import_flags():
	if not os.exists(JSON):
		return
	global flags
	data = json.loads(JSON)
	print(data)

def main():
	# TODO: import solved flags from json
	for lvl in [str(n).zfill(2) for n in range(LEVELS_SOLVED)]:
		try:
			connection = SSHConnection(
				IP,
				PORT,
				f"level{lvl}",
				flags.get(prev, "level00")
			)
			level_solver = importlib.import_module(f"level{lvl}.resources.level{lvl}")
			flag, password = level_solver.solve(connection)
			if flag and password:
				flags[f"flag{lvl}"] = flag
				flags[lvl] = password
				prev = lvl
				json.dump(flags, open(JSON, "w"))
				print(f"Level {lvl} solved! Flag: {password}")
			else:
				print(f"Level {lvl} not solved.")
			connection.close()
		except Exception as e:
			print(f"Level {lvl} not solved: {e}")
			exit(1)

if __name__ == "__main__":
	main()