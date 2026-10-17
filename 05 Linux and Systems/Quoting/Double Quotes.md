---
tags: [cli]
created: 2025-09-15
publish: true
---
Stop the shell from interpreting **some** metacharacters (special characters) , including glob chars.

***Glob characters, aka wild cards, are symbols that have special meaning to the shell; they are interpreted by the shell itself before it attempts to run any command. Glob characters include the  `*` , `?` , `[ ]`, among others.

Within double quotes, glob chars are shown like in normal text (or like strings in programming). In the `echo` below, the [[Bash]] shell doesnt convert the glob into filenames that match the pattern.
<!-- embed removed: Pasted image 20230601203221.png (file not in vault) -->

Double quotes still allow for command substitution, variable substitution, and permit some other shell metachars not discussed yet.
Value of the `PATH` variable is still displayed:
<!-- embed removed: Pasted image 20230601203423.png (file not in vault) -->

##### On backquotes
Double quote chars have no effect on [[Backquotes]]. The shell will still use them as command substitution.
`` echo This is the command "`date`"
<!-- embed removed: Pasted image 20230610145501.png (file not in vault) -->

##### On wildcard chars
" will still have and effect on wildcard chars, disabling their special meaning.
<!-- embed removed: Pasted image 20230610145715.png (file not in vault) -->

