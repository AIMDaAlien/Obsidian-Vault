[[External Commands]] are binary executables stored in directories that are searched by the [[Shell]]. If a user types `ls`, the shell searches through the directories that are listed in  `PATH` variable to try to find a file named `ls` that can be executed. 
Use `which` to show the full path to `ls`

`which ls` 
![[Pasted image 20230609140342.png]]

For external commands, the `type` cmd shows the location of the cmd:
![[Pasted image 20230609140435.png]]

The output of `type` might differ significantly from the output of `which`:
![[Pasted image 20230609142650.png]]

Using the -a option of the `type` cmd shows all locations tha contain the command.
![[Pasted image 20230609145648.png]]

