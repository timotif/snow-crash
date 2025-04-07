from solver.utils import caesar_cipher, getflag

def solve(connection) -> str | None:
	flag00_files = connection.exec("find / -user flag00 2>/dev/null")
	for file in flag00_files.split():
		try:
			if file.startswith("/proc"):	# Skip /proc files
				continue
			content = connection.exec(f"cat {file} 2>/dev/null")
			if not content or content.startswith("Error:"):
				continue
			flag_password = caesar_cipher(content, -15)
			flag = getflag("00", flag_password)
			if flag:
				return flag_password, flag
		except Exception as e:
			continue
	return None
