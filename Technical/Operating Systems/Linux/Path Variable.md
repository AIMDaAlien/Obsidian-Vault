The `PATH` variable is an essential [[Bash]] shell variable which contains a list that defines which [[Directories inside Linux file system]] the shell looks in to find cmds. If a valid cmd is entered and the shell returns a "command not found", its because the Bash shell was unable to locate a cmd by that name in any directories in that path. 

The following command displays the path of the current shell:
`echo $PATH`

Each directory in the lit is separated by a : . Based on the preceding output, the path contains the following directories in the order they're listed. 
/home/sysadmin/bin
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
/sbin
/bin
/usr/games

![[Pasted image 20230529092540.png]]


If custom software is installed, it may be necessary to modify the `PATH` to make it easier to execute these commands. For example, the following will add and verify the `/usr/bin/custom` directory to the `PATH` variable:

`PATH=/usr/bin/custom:$PATH`
`echo $PATH`        -->        ``/usr/bin/custom:/home/sysadmin/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

######      When updating the `PATH` variable, always include the current path to not lose access to commands located in those directories. This can be accomplished by appending `$PATH` to the value in the assignment expression. Recall that a variable name preceded by a dollar sign represents the value of the variable.



#linux 