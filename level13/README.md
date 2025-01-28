## level13

We’re presented to a binary

```bash
level13@SnowCrash:~$ ./level13
UID 2013 started us but we we expect 4242
level13@SnowCrash:~$ id
uid=2013(level13) gid=2013(level13) groups=2013(level13),100(users)
```

Is there a real check? The `uid` is indeed correct…

```bash
level13@SnowCrash:~$ ltrace ./level13
__libc_start_main(0x804858c, 1, 0xbffff7b4, 0x80485f0, 0x8048660 <unfinished ...>
getuid()                                                                                                                      = 2013
getuid()                                                                                                                      = 2013
printf("UID %d started us but we we expe"..., 2013UID 2013 started us but we we expect 4242
)                                                                           = 42
exit(1 <unfinished ...>
+++ exited (status 1) +++
```

Not much in the `ltrace`. How about `gdb`?

```bash
   0x08048595 <+9>:	  call   0x8048380 <getuid@plt>
=> 0x0804859a <+14>:	cmp    $0x1092,%eax # here's the check
   0x0804859f <+19>:	je     0x80485cb <main+63>
```

While at it, we can set a breakpoint and modify the value of the register right before the check to change the program flow.

```bash
(gdb) info registers $eax
eax            0x7dd	2013
(gdb) set $eax=0x1092
(gdb) info registers $eax
eax            0x1092	4242
```

`ft_des` is hashing the flag (that otherwise would be clearly visible with `strings level13`)

```bash
level13@SnowCrash:~$ strings level13
[...]
UID %d started us but we we expect %d
boe]!ai0FB@.:|L6l@A?>qJ}I # this is the value do decrypt
your token is %s
[...]
```

We can see that the return value of `ft_des` is stored in `$esp+4` so it’s the %s in the printf

```bash
   0x080485d2 <+70>:	call   0x8048474 <ft_des>
   0x080485d7 <+75>:	mov    $0x8048709,%edx
   0x080485dc <+80>:	mov    %eax,0x4(%esp)
   0x080485e0 <+84>:	mov    %edx,(%esp)
   0x080485e3 <+87>:	call   0x8048360 <printf@plt>
   0x080485e8 <+92>:	leave
   0x080485e9 <+93>:	ret
```

Then we can just see what string is at that memory address

```bash
(gdb) break *main+75
Breakpoint 2 at 0x80485d7
(gdb) c
Continuing.

Breakpoint 2, 0x080485d7 in main ()
(gdb) x/s $eax
0x804b008:	 "2A31L79asukciNyi8uppkEuSx"
```