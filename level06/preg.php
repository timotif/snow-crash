<?php
$a = "Hello world";
$a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);

echo $a;
?>