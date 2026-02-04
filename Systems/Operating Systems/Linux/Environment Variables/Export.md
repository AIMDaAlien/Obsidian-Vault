##### Exporting allows the var to be accessible by other programs.
![[Pasted image 20230621195102.png]]
****Refer back to [[printenv]]***

The `export` command is used to turn a local variable into an environment variable.
`export variable

After exporting `variable 1 ` its now an environment variable. You can now find it in the search through the environment variables.
`export variable1 `
`env | grep variable1`      -->    `variable1=Something

The `export` command can also make a variable an environment variable upon its creation by using the assignment expression as the argument:
`export variable2='Else'
`env | grep variable2`       -->    `variable2=Else`


To change the value of an environment variable, use the assignment expression:
`variable1= $variable1 $ variable2 `
`echo $variable1`      -->     `Something Else`

Exported variables can be removed using the `unset` command:
`unset variable2 ` 


#CLI 