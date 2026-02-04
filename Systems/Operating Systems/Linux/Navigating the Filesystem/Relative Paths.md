Relative paths start from the current directory. It gives directions to a file to the current directory in the filesystem. They don't start with / but rather with the name of the directory contained within the current directory. 

The argument is an example of the simplest relative path
![[Pasted image 20230617215000.png]]

If the user is located in the `Documents` directory, moving to the `Art` directory can be accomplished in a few ways. 

![[Pasted image 20230617215100.png]]

Using the [[Absolute Paths]]:
![[Pasted image 20230617215146.png]]

Or multiple relative paths:
![[Pasted image 20230617215208.png]]

But simplest would be to use a single relative path that covers the origin to the destination directory.:
![[Pasted image 20230617215259.png]]
![[Pasted image 20230619045956.png]]

Use [[pwd]] to confirm you are in the path.

#CLI #linux 