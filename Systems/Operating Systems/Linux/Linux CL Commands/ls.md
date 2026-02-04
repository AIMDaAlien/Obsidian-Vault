Is used to list info about directories and files. By default it shows info for the current directory.
Use `-l`  to shoe this info in the long format which gives additional info about files located in the current working directory.

`ls -l`
The output should look like:
![[Pasted image 20230607203808.png]]

*Note that directories are considered a type of file in the Linux file system.*

Arguments can be added to cmds as well. Adding the location of a specific directory to the `ls` cmd lists info for that directory.
Use `/tmp` to display detailed info about files in the `/tmp` directory.

`ls -l /tmp`
Output should be 
![[Pasted image 20230607204155.png]]
We now see there's a file called `inside_setup.sh` inside it. 

The ? Char can be used to match exactly one char in a file name. 
`ls -d /etc/????`
![[Pasted image 20230619061732.png]]

By using [] you can specify a char to match from a set of chars.
display all files in `/etc` directory that begin with the letters `a`, `b`, `c` or `d`:
`ls –d /etc/[abcd]*`
![[Pasted image 20230619061939.png]]



#### Colors
![[Pasted image 20230619055313.png]]
Colors indicate what type the item is.









#CLI 