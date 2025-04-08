from solver.config import * 
from solver.ssh import SSHConnection
import json
import importlib
import os

flags = {"-1": "level00"}

def import_flags():
	if not os.path.exists(JSON):
		return
	global flags
	with open(JSON, "r") as f:
		flags = json.load(f)

def parse_levels():
	levels = os.getenv("LEVEL").lower()
	print("Selected levels:", levels)
	if not levels:
		raise ValueError("LEVEL environment variable not set.")
	if levels == "all":
		return range(LEVELS_SOLVED)
	elif levels == "mandatory":
		return range(10)
	elif levels == "bonus":
		return range(10, LEVELS_SOLVED)
	elif "-" in levels:
		start, end = levels.split("-")
		return range(int(start), int(end) + 1)
	elif "," in levels:
		return levels.split(",")
	else:
		return [levels]

def find_last_level():
	for lvl in range(LEVELS_SOLVED):
		if not flags.get(str(lvl).zfill(2)):
			return str(lvl - 1).zfill(2)
	return str(lvl).zfill(2)

def main():
	import_flags()
	for lvl in [str(n).zfill(2) for n in parse_levels()]:
		prev = find_last_level()
		if lvl != "00" and int(lvl) - 1 > int(prev):
			print(f"Level {str(int(lvl) - 1).zfill(2)} not solved yet: cannot connect to level {lvl}.")
			print(f"Last solved level: ", end="")
			print("No level solved" if prev == "-1" else prev)
			continue
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
				print(f"Level {lvl} solved! Flag: {flag}", flush=True)
			connection.close()
		except Exception as e:
			print(f"Level {lvl} not solved: {e}")
			exit(1)

if __name__ == "__main__":
	main()