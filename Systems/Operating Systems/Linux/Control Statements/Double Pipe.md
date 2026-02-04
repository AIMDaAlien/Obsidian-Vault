`command1 || command2`

###### The double pipe `||` is a logical "or". Depending on the result of the first command, the second command will either run or be skipped.

Youre basically telling the shell "either run this first command or the second". 

In the following example, the `echo` command only executes if the `ls` command fails:
![[Pasted image 20230602095116.png]]

Failure before the "or" statement causes the cmd to execute; however, a successful first statement causes the cmd to not execute:
``false || echo Fail Or``
``true || echo Nothing to see here
![[Pasted image 20230610151224.png]]
