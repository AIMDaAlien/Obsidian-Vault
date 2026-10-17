---
tags: [cli]
created: 2025-09-15
publish: true
---
There's also an alternative to [[Single Quotes]] a single char. Consider the follwing message:
`The service costs $1 and the path is $PATH`

If this sentence is placed in [[Double Quotes]], `$1` and `$PATH` are considered variables.
<!-- embed removed: Pasted image 20230601221728.png (file not in vault) -->

If it is placed in single quotes, `$1` and `PATH` are not considered as variables.
<!-- embed removed: Pasted image 20230601222001.png (file not in vault) -->

***But what if you want to have `$PATH` treated as a variable and `$1` not?***
*In this case, use a backslash `\` character in front of the dollar sign `$` character to prevent the shell from interpreting it. The command below demonstrates using the `\` character:

<!-- embed removed: Pasted image 20230601222123.png (file not in vault) -->

You can also place a backslash char in fron t of each [[Backquotes]].
``echo This is the command \`date\`
<!-- embed removed: Pasted image 20230610145308.png (file not in vault) -->

