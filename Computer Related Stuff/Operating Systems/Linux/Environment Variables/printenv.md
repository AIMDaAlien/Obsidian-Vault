#### Creating new environment variables
New variables can be created by typing a new variable name and assigning it a value in ("") separated by =. When the var is created, use  `echo`. 
$ must precede the var name while showing the value using echo. Not required while creating the var though.
![[Pasted image 20230621194735.png]]

**printenv** *prints all or the specified environment variables*. 

Now that we created a new env var, lets try finding it in the list of variables displayed by the printenv cmd, and printing out its value. 

This can be done by using [[grep]]. 
![[Pasted image 20230621194750.png]]
No output is shown because we have yet to "[[Export]]" it into the file containing the names of all variables. 