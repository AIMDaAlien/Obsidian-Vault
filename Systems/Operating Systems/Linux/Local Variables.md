
*Local  or shell variables* only exist in the current shell. When the user closes a terminal window or shell, all of the variables are lost.
They are often associated with user based tasks and are lowercase by convention.

The `echo` command is used to display output int the terminal. To display the value of the variable, use `$` followed by the variable name as an argument

The following example creates a local variable named `variable1` and assigns it a value of `Something`. 
`variable1='Something'
`echo $variable1`        -->       `Something`

###### Linux uses `echo` just as how Python uses [[Print Function]]




#linux #CLI 