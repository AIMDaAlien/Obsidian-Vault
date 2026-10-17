---
tags: [cli]
created: 2025-09-15
publish: true
---
###### Backquotes or backticks are used to specify a cmd within a cmd, a process called *command substitution*.

 Note the output of the `date` cmd:
<!-- embed removed: Pasted image 20230601222556.png (file not in vault) -->

Now note the output of the `echo` cmd:
<!-- embed removed: Pasted image 20230601222622.png (file not in vault) -->

In the previous cmd, the word *date*  is treated as regular text, and the shell passes *date*  to the `echo` cmd.
**To execute `date` and have the output of that cmd sent to the `echo` cmd, put the `date` cmd between two backquote chars:
<!-- embed removed: Pasted image 20230601222909.png (file not in vault) -->

You can also place $(before and ) after the cmd to get command substitution:
`echo Today is $(date)`

<!-- embed removed: Pasted image 20230610142930.png (file not in vault) -->

**Backquotes look very similar to single quotes thus a later version of [[Bash]] made this new format to make it more visually clear.**

