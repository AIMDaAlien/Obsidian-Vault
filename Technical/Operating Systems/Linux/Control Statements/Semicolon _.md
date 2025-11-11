```d
```command1; command2; command3
```

The ; can be used to run multiple cmds, one after the other. Each cmd runs independently and consecutively; regardless of the result of the first cmd, then the second runs when first finishes, then so on.

For example, to print the months of January, February and March of 2030, execute the following command:
![[Pasted image 20230601223754.png]]

``echo Hello; echo Linux; echo Student
![[Pasted image 20230610145921.png]]
Three commands are executed sequentially


#### Error

``false; echo Not; echo Conditional
![[Pasted image 20230610150051.png]]
While you havent seen the output of the `false` cmd, it did execute. However, when cmds are separated by ; char, they are completely independent of each other. 

