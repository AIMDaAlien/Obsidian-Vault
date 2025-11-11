Linux inherited the unix model of file ownership and permissions. Every file has a set of permissions.

**User**
**Group
Other** 

![[Pasted image 20230526162609.png]]
The first column indicates if we're talking about a [[Directories inside Linux file system]] ( d ),  file ( - ), or link ( l ).

The second column refers to the user rights. This is the owner of the file, directory or link and these three characters determine what the owner can do. These are the permissions for the owner of the file or directory

The next three are permissions for the group that the file is owned by and the final three characters define access perms for the "others".

**r**  read perms
**w**  write perms
**x**   executable

**-rw-------**:      A file only accessible by its owner

**-rwxr-xr-x**:       A file thats executable by every user on the system (world-executable) file.

**-rw-rw-rw-**:        A file thats open to modification by every user on the system (world-writable) file. 

**drwxr-xr-x**:        A file that every user on the system can read and access.

**drwxrwx---**:        A directory thats modifiable (including its contents) by its owner and group. 

**drwrxr-x---**:       A directory thats accessible by its group.




#linux 