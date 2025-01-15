from solver.config import * 
from solver.ssh import SSHConnection
import json
import importlib

flags = {}
prev = "00"

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
		if password:
			flags[f"flag{lvl}"] = flag
			flags[lvl] = password
			prev = lvl
			json.dump(flags, open(JSON, "w"))
			print(f"Level {lvl} solved! Flag: {password}")
		else:
			print(f"Level {lvl} not solved.")
		connection.close()
	except Exception as e:
		print(e)
		exit(1)