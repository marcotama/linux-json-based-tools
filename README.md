This suite of tools is meant to replace some of the Linux most commonly used commands.
The advantage is that all of these commands write their output on stdout in JSON format,
which allows for easy processing.

The suite contains the following tools:
* `ldc` (List Directory Content): replaces `ls`.
* `lp` (List Processes): replaces `ps`
* `filter`: replaces `grep`
* `tab`: prints the JSON input into a readable table format
* `lf`: lists the fields in the JSON input

Assuming the aliases in `init.sh` are setup, the following usages are possible:

```
$ ldc | lf
access-rights access_rights device ...
```

```
$ lp | lf
arg_end arg_start blocked ...
```

```
$ ldc | tab name is-file
.git                       0
TODO.txt                   1
filter.py                  1
...
```

```
$ ldc | filter 'is-file == 1' | tab name size
TODO.txt                     15
filter.py                  5353
list_fields.py              712
...
```

```
$ ldc | tab name size  --headers
name                         size
.git                         4096
TODO.txt                       15
filter.py                    5789

...
```

```
$ lp | filter "real_uid == `id -u`" 'cmdline =~ "^python.+"' | tab pid cmdline
15173  python list_processes.py
15174  python filter.py real_uid == 1000 cmdline =~ "^python.+"
15176  python tab.py pid cmdline
```

```
$ ldc | tab `ldc | lf`
755  16877  2053  1  1  0  1000  5  1803287  0  0  0  1  0  0  0  0  1489801354  1489801354  1489801354  0  .git                       8  1  1  0  5  .  0  0  4096  0  1  1  1  1000  7
644  33188  2053  0  1  0  1000  4  1720053  0  0  0  0  0  1  0  0  1489796819  1489796775  1489796775  0  TODO.txt                   1  0  1  0  4  .  0  0    15  0  0  1  1  1000  6
644  33188  2053  0  1  0  1000  4  1720045  0  0  0  0  0  1  0  0  1489801163  1489801162  1489801162  0  filter.py                  1  0  1  0  4  .  0  0  5789  0  0  1  1  1000  6
...
```