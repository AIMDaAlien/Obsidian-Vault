Determines if there's an executable file . In this case, date that is located within a directory listed in the `PATH` value. (Also see [[Environment Variables]])

`which date`

Output should look like:
![[Pasted image 20230608214312.png]]

The output of `which`  tells you that when you execute `date`, the system will run the cmd `/bin/data`. The `which` cmd makes use of the `PATH` variable to determine the location of the `date` cmd.
