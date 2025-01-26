## level09

We have again a binary and a token. The binary wants one argument, and if we provide token we get an output, suspiciously short for a flag token. Some encryption?

I try to create arbitrary files and run them through the script:

```bash
level09@SnowCrash:~$ echo "my content\n" > /tmp/foo
level09@SnowCrash:~$ echo "my content\n" > /tmp/bar
level09@SnowCrash:~$ ./level09 /tmp/foo
/uos3kuv
level09@SnowCrash:~$ ./level09 /tmp/bar
/uos3ggy
```

The content is the same but the output is different… so maybe the filename is also factored into the encryption?

A check with `ltrace` tells me not to reverse engineer the file

```bash
level09@SnowCrash:~$ ltrace ./level09 token
__libc_start_main(0x80487ce, 2, 0xbffff6e4, 0x8048aa0, 0x8048b10 <unfinished ...>
ptrace(0, 0, 1, 0, 0xb7e2fe38)                                                                                       = -1
puts("You should not reverse this"You should not reverse this
)                                                                                  = 28
+++ exited (status 1) +++
```

More experiments tell me that the binary considers **only** the path/filename: changing the content does not change the encrypted output

```bash
level09@SnowCrash:~$ echo "a" > /tmp/foo
level09@SnowCrash:~$ ./level09 /tmp/foo
/uos3kuv
level09@SnowCrash:~$ ./level09 /tmp/bar
/uos3ggy
level09@SnowCrash:~$ echo "a" > /tmp/fos
level09@SnowCrash:~$ ./level09 /tmp/fos
/uos3kuz
level09@SnowCrash:~$ echo "b" > /tmp/fos
level09@SnowCrash:~$ ./level09 /tmp/fos
/uos3kuz
```

… and more experiments tell me that it’s not even working with files: it just shifts each char increasingly. 

```bash
level09@SnowCrash:~$ ./level09 bla
bmc
level09@SnowCrash:~$ ./level09 b
b
level09@SnowCrash:~$ ./level09 ba
bb
level09@SnowCrash:~$ ./level09 baa
bbc
level09@SnowCrash:~$ ./level09 aaaaaaaaaaaaa
abcdefghijklm
```

`token` is actually readable this time, but it contains non ASCII chars.

It seems plausible to think that it was encrypted using the given binary: it would decrease the non-ascii getting them probably in range…

I got the exact token with `xxd token` 

I wrote a Python script to reverse the encryption

```python
# Non-ASCII chars are not allowed in literal strings, even byte strings like this
token = b"\x66\x34\x6b\x6d\x6d\x36\x70\x7c\x3d\x82\x7f\x70\x82\x6e\x83\x82\x44\x42\x83\x44\x75\x7b\x7f\x8c\x89"

for i, byte in enumerate(token):
	print(chr(byte - i), end='')
```