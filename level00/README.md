### level00

```bash
# Trying to connect as flag00 with su flag00: need password.
level00@SnowCrash:~$ su flag00
Password: 
su: Authentication failure
```

Looking for occurrencies of user flag00: `find / -user flag00 2>/dev/null`

```bash
# Looking for occurrencies of user flag00
level00@SnowCrash:~$ find / -user flag00 2>/dev/null
/usr/sbin/john
/rofs/usr/sbin/john
level00@SnowCrash:~$ ll /usr/sbin/john 
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /usr/sbin/john
level00@SnowCrash:~$ cat /usr/sbin/john 
cdiiddwpgswtgt
# BINGO!
level00@SnowCrash:~$ su flag00
Password: 
su: Authentication failure
# Oooops...
```

I guess it’s encrypted somehow… Checking https://dencode.com/

Assuming it might be Ceasar since we’re at level 00… Playing around with the offset to see if something rings a bell… until https://dencode.com/cipher/caesar?v=cdiiddwpgswtgt&shift=15 gives `nottoohardhere`

```bash
level00@SnowCrash:~$ su flag00
Password: 
Don't forget to launch getflag !
flag00@SnowCrash:~$ getflag
Check flag.Here is your token : x24ti5gi3x0ol2eh4esiuxias
```

### External resources
- https://dencode.com/

### Key Learnings
Basic file enumeration using find
Simple cryptography - Caesar cipher with shift 15
Importance of trying basic encryption methods first