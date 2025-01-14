## level01

```bash
# The password seems visible
level01@SnowCrash:~$ cat /etc/passwd
[...]
flag00:x:3000:3000::/home/flag/flag00:/bin/bash
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
flag02:x:3002:3002::/home/flag/flag02:/bin/bash
[...]
# ... but it's wrong
level01@SnowCrash:~$ su flag01
Password: 
su: Authentication failure
```
```bash
# A better way to get the flag01 password directly would have been
level01@SnowCrash:~$ getent passwd flag01
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

Researching more on `/etc/passwd` 

[Understanding /etc/passwd File Format](https://www.cyberciti.biz/faq/understanding-etcpasswd-file-format/)

When the hash in `/etc/passwd` has no prefix it could be the DES algorithm.

I try to decrypt with JohnTheRipper

https://www.openwall.com/john/

```bash
# Saving the hash into a file
┌──(root㉿c47d3ce781b5)-[/]
└─# echo "42hDRfypTqqnw" > passwd

# Calling john on it
┌──(root㉿c47d3ce781b5)-[/]
└─# john passwd 
Created directory: /root/.john
Using default input encoding: UTF-8
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 256/256 AVX2])
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
abcdefg          (?)     
1g 0:00:00:00 DONE 2/3 (2025-01-14 17:12) 25.00g/s 614400p/s 614400c/s 614400C/s 123456..HALLO
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 

# Even without wordlist it did it in a second: abcdefg
```

I can now log into the flag01 profile and get my flag

```bash
level01@SnowCrash:~$ su flag01
Password: 
Don't forget to launch getflag !
flag01@SnowCrash:~$ getflag
Check flag.Here is your token : f2av5il02puano7naaf6adaaf
```

### External resources
- John the Ripper - https://www.openwall.com/john/

### Key Learnings
- getent command in Linux
- Understanding /etc/passwd File Format
- Using John the Ripper to crack DES hashes