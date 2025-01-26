from solver.config import * 
from solver.ssh import SSHConnection
import json
import importlib
import os

flags = {"start": "level00"}
prev = "start"

def import_flags():
	if not os.path.exists(JSON):
		return
	global flags
	with open(JSON, "r") as f:
		flags = json.load(f)

def main():
	# TODO: force computing without retrieving flags
	import_flags()
	global prev
	for lvl in [str(n).zfill(2) for n in range(LEVELS_SOLVED)]:
		if flags.get(lvl):
			prev = lvl
			print(f"Level {lvl} solved! Flag: {flags.get(lvl)}")
			continue
		try:
			connection = SSHConnection(
				IP,
				PORT,
				f"level{lvl}",
				flags.get(prev)
			)
			level_solver = importlib.import_module(f"level{lvl}.resources.level{lvl}")
			token, flag = level_solver.solve(connection)
			if not flag:
				print(f"Level {lvl} not solved.")
			else:
				if token:
					flags[f"flag{lvl}"] = token
				flags[lvl] = flag
				prev = lvl
				json.dump(flags, open(JSON, "w"))
				print(f"Level {lvl} solved! Flag: {flag}")
			connection.close()
		except Exception as e:
			print(f"Level {lvl} not solved: {e}")
			exit(1)

if __name__ == "__main__":
	main()