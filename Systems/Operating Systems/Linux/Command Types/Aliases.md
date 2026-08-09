###### Used to map larger cmds to shorter key sequences. When the shell sees an alias being executed, it substitutes the longer sequence before proceeding to interpret cmds. 

For example, the cmd `ls -l` is commonly aliased as `l` or `ll`.  Because these smaller cmds are easier to type, it becomes faster to run the `ls -l` cmd line.

To determine what aliases are set on the current shell, use `alias`:
![[Pasted image 20230601105844.png]]

The aliases were created by initialization files which are designed to make the process of creating aliases automatic.

New aliases can be created by using the following format, where `name` is the name to be given to alias and `command` is the cmd to be executed when the alias is run.
`alias name=command`

For example, the `cal 2019` command shows the calendar for 2019. Suppose you run this command often. Instead of executing the full cmd each time, you can create an alias called `mycal` and run the alias:
![[Pasted image 20230601105725.png]]

Aliases created this way only persist while the shell is open. When the shell closes, the new aliases are lost. Each shell has its own aliases. 

The `type` command can identify aliases to other commands:
![[Pasted image 20230601110037.png]]
The output of these commands indicates that `ll` is an alias for `ls -alF`, and even `ls` is an alias for `ls --color=auto`.