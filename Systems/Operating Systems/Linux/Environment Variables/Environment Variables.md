*Environment variables, aka global variables* are available system-wide in all shells used by [[Bash]] when interpreting commands and performing tasks. The system automatically recreates environment variables when new [[Shell]] are opened. 

In simple words, [[Variables]] are defined only in a particular block. Outside that block, it's undefined. 

Examples include, the `PATH`, `HOME`, and `HISTSIZE` variables.
The `HISTSIZE` variable defines how many previous commands to store in the [[History]] list. 
below displays the value of the `HISTSIZE` variable:

``echo $HISTSIZE`  --> 1000 ``

To modify the value of an existing variable, use the assignment expression:

``HISTSIZE=500
``echo $HISTSIZE   -->500


When run with no arguments, the `env` command outputs list of environmental variables. Because the output of `env` can be long, the examples use a text search to filter output.+


In a previous example, `variable1` was created as a [[Local Variables]] so the following search in the environment variables results in no output:
``env | grep variable1``

###### The pipe `|` character passes the output of the `env` command to the `grep` command, which searches the output.

In order to handle system level info, you must define the set of environment variables. [[env Commands]]






#linux #CLI 