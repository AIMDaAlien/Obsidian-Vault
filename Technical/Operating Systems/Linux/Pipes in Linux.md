![[Pasted image 20230621201150.png]]

With pipes, you can connect multiple cmds to chain simpler, repetitive tasks and create new solutions. 

The pipe takes the output from one cmd and uses it as input for another and can be stacked. 

The most basic purpose is to filter out info that you dont want. Popular case would be a scenario of finding and sorting strings and words inside a doc, done by piping the output to grep and sort cmds,  respectively.


![[Pasted image 20230621201231.png]]
Suppose we have a directory full of different types of files. We want to know how many files of a certain type are in that directory. 

Easiest way to count files in a directory on Linux is to use [[ls]] cmd and pipe it with ``wc -l`` cmd. `wc` is used to print the bytes, chars, or newlines count.
In this case, we are using this cmd to count the number of files in a directory. 


