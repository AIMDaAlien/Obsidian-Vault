###### The double ampersand `&&` acts as a logical "and"; if the first command is successful, then the second cmd will also run. If the first cmd fails, then the second cmd wont run.

Consider first the concept of failure and success for commands. For example, consider the `ls` cmd. It succeeds if the given directory is accessible and fails if it isnt. 

In the following example, the first command succeeds because the `/etc/ppp` directory exists and is accessible while the second command fails because there is no `/junk` directory:
![[Pasted image 20230601224155.png]]

To use the success or failure of the `ls` command in conjunction with `&&` execute commands like the following. In the first example, the `echo` command is executed because the `ls` command succeeds:
![[Pasted image 20230601224320.png]]


### Errors

In the second example, the `echo` command isn't executed because the `ls` command fails: 
![[Pasted image 20230601224415.png]]

``echo Success && false && echo Bye
![[Pasted image 20230610150815.png]]
The first `echo` succeeds and we see its output. The `false` cmd executes with failing result thus the last `echo` isnt executed. 

#CLI 