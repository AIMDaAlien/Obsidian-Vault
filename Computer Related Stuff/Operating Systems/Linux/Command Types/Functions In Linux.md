Functions can also be built using existing cmds to either create new cmds or to override cmds bult-in to the shell or cmds stored in files. **[[Aliases]] and functions are normally loaded from the initialization files when the shell first starts. 


Functions are more advanced than aliases and typically are used in [[Bash]] [[Shell]] scripts. To create a function, the following syntax is used:
```
function_name () 
{
   commands
}
```

In the format above, *function_name* can be anything that the admin wants to call the function. The cmds that the admin wants to execute can replace the `commands` placeholder.

*Note the formatting. In particular, the location of the () and {} , as well as the convention of using tabs to make the function more easily readable.*

Functions are useful as they allow for a set of cmds to be executed one at a time rather than typing cmds repeatedly. 
     In the example below, a function called `my_report` is created to execute the `ls`, `date`, and `echo` commands.

![[Pasted image 20230601202014.png]]

When creating a function, > will show as a prompt to enter the cmds for the function. {} are used to let the shell know when function begins and ends > to exit the prompt.

Once a function is created, the function name may be invoked from the BASH prompt to execute the function:

![[Pasted image 20230601202230.png]]
