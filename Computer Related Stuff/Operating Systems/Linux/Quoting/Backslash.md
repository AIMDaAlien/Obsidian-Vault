There's also an alternative to [[Single Quotes]] a single char. Consider the follwing message:
`The service costs $1 and the path is $PATH`

If this sentence is placed in [[Double Quotes]], `$1` and `$PATH` are considered variables.
![[Pasted image 20230601221728.png]]

If it is placed in single quotes, `$1` and `PATH` are not considered as variables.
![[Pasted image 20230601222001.png]]

***But what if you want to have `$PATH` treated as a variable and `$1` not?***
*In this case, use a backslash `\` character in front of the dollar sign `$` character to prevent the shell from interpreting it. The command below demonstrates using the `\` character:

![[Pasted image 20230601222123.png]]

You can also place a backslash char in fron t of each [[Backquotes `]].
``echo This is the command \`date\` 
![[Pasted image 20230610145308.png]]






#CLI