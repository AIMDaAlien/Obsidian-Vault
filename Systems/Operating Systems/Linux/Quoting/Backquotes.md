###### Backquotes or backticks are used to specify a cmd within a cmd, a process called *command substitution*. 
 
 Note the output of the `date` cmd:
![[Pasted image 20230601222556.png]]

Now note the output of the `echo` cmd:
![[Pasted image 20230601222622.png]]

In the previous cmd, the word *date*  is treated as regular text, and the shell passes *date*  to the `echo` cmd. 
**To execute `date` and have the output of that cmd sent to the `echo` cmd, put the `date` cmd between two backquote chars:
![[Pasted image 20230601222909.png]]

You can also place $(before and ) after the cmd to get command substitution:
`echo Today is $(date)`

![[Pasted image 20230610142930.png]]

**Backquotes look very similar to single quotes thus a later version of [[Bash]] made this new format to make it more visually clear.**




#CLI 