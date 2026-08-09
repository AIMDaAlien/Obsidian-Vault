Binary executables stored in directories that are searched by the shell. If a user types the `ls` cmd, then the shell searches through the directories that are listed in the `PATH` variable to try to find a file named `ls` that it can execute. 

If a cmd misbehaves, or is not accessible, it is helpful to know where the shell is finding the cmd or which version it's using. It'd be tedious to look in directories listed in `PATH`  variable. Instead, [[which]]  cmd displays the full path to the cmd in question:

`which command` 

This searches for the location of a cmd by searching the `PATH` .

```Linux
sysadmin@localhost:~$ which ls                                       
/bin/ls                                                               
sysadmin@localhost:~$ which cal                                        
/usr/bin/cal
```


External cmds can also be executed by typing the complete path to the cmd. For example, to execute `ls`:
`/bin/ls`

The `type` cmd displays the location of the 
```sysadmin@localhost :~$ type cal                                      
cal is /usr/bin/cal
```

In some cases the output of the `type` command may differ significantly from the output of the `which` command:
```
sysadmin@localhost:~$ type echo                                     
echo is a shell builtin
sysadmin@localhost:~$ which echo                                        
/bin/echo
```

Using `-a` of the `type` command displays all locations that contain the command:
```
sysadmin@localhost:~$ type -a echo                                      
echo is a shell builtin                                                
echo is /bin/echo
```




#linux 