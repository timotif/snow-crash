## level14

This time we have nothing in the home directory, but the trick we just used with `gdb` maybe can be pulled off on `getflag` itself…

```bash
level14@SnowCrash:~$ gdb getflag
GNU gdb (Ubuntu/Linaro 7.4-2012.04-0ubuntu2.1) 7.4-2012.04
Copyright (C) 2012 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i686-linux-gnu".
For bug reporting instructions, please see:
<http://bugs.launchpad.net/gdb-linaro/>...
Reading symbols from /bin/getflag...(no debugging symbols found)...done.
(gdb) disas main
Dump of assembler code for function main:
	 [...]
   0x08048989 <+67>:	call   0x8048540 <ptrace@plt>
   0x0804898e <+72>:	test   %eax,%eax
   [...]
```

There’s a protection in place to avoid exactly what we are doing: `ptrace` can be attached to a process once, so if we run `getflag` with a debugger that uses `ptrace` another call to the function will return `-1`. That’s exactly the case.

So let’s trick this check…

```bash
(gdb) break *main+72
Breakpoint 1 at 0x804898e
(gdb) r
Starting program: /bin/getflag

Breakpoint 1, 0x0804898e in main ()
(gdb) info registers $eax
eax            0xffffffff	-1
(gdb) set $eax=0
(gdb) info registers $eax
eax            0x0	0
```

Next important check is the uid: we’re still running the program as `level14` but we need to do so as `flag14`.

```bash
level14@SnowCrash:~$ cat /etc/passwd
[...]
level14:x:2014:2014::/home/user/level14:/bin/bash
[...]
flag14:x:3014:3014::/home/flag/flag14:/bin/bash
```

There is one call to `getuid` in `main`: it has to be that…

```bash
   0x08048afd <+439>:	call   0x80484b0 <getuid@plt>
   0x08048b02 <+444>:	mov    %eax,0x18(%esp)
   
(gdb) break *main+444
Breakpoint 2 at 0x8048b02
(gdb) c
Continuing.

Breakpoint 2, 0x08048b02 in main ()
(gdb) info registers $eax
eax            0x7de	2014
(gdb) set $eax=3014
(gdb) info registers $eax
eax            0xbc6	3014
(gdb) c
Continuing.
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
[Inferior 1 (process 3090) exited normally]
```

This is the token for `flag14`.

```bash
level14@SnowCrash:~$ su flag14
Password:
Congratulation. Type getflag to get the key and send it to me the owner of this livecd :)
flag14@SnowCrash:~$ getflag
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
```