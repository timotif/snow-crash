from solver.utils import caesar_cipher, getflag

def solve(connection) -> str | None:
	flag00_files = connection.exec("find / -user flag00 2>/dev/null")
	content = connection.exec(f"cat {flag00_files.split()[0]}")
	flag_password = caesar_cipher(content, -15)
	flag = getflag("00", flag_password)
	if flag:
		return flag_password, flag
	return None
