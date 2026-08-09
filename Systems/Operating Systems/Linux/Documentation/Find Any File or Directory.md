`whereis` cmd (from [[Where Are These Commands Located]]) is specifically made to find cmds and man pages but not files or directories.

To find file or directory, use `locate` to search a database of all files and directories that were on the system when the database was created.

![[Pasted image 20230611145846.png]] 
Typically the cmd to generate this database is run every night.

**Any files created today wont be searchable with `locate`. If root perms, you can update the `locate` database manually by running `updatedb`. Normal users cant update db file and when running `locate`, the output may be limited due to file perms.**

The output of `locate` can be large and can produce every  file that contains whatever string (such as `passwd`), not just files named passwd.

***Should start by finding how many files match using `-e` to `locate`***
![[Pasted image 20230611150821.png]]

To limit the output, use `-b` whch only includes listings that have the search term in the basename (portion of filename not included in directory names) of the filename. 
![[Pasted image 20230611151013.png]]

To limit output even furthrer place a / char in front of the search term. This char limits the output to filenames that exactly match the term:
![[Pasted image 20230611151147.png]]





#linux 
