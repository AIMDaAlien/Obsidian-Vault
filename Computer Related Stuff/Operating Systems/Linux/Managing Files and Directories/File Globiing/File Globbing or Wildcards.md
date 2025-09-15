Limits which files or directories you see. For example, * char can match "zero or more characters" in a filename. Execute the following cmd to show only the files that start with the letter s in `/etc` directory:
``ls -d /etc/s*``

![[Pasted image 20230619061439.png]]

***Note that the `-d` option prevents files from subdirectories from being displayed. It should always be used with the `ls` command when you are using file globbing.

Globs are powerful because they allow you to specify patterns that match filenames in a directory. So instead of manipulating a single file, you can easily execute commands that affect many files. 
Glob characters are interpreted by the shell itself before it attempts to run any command. As a result, glob characters can be used with any command.

[[Asterisk]]
[[Question Mark]]

#linux 