The directory where you first find yourself in when you login is called **[[~ Home Directory]]**. Most of the work you'll do will be in the home directory and its subdirectories to organize files.
[[What are directories]]  
[[Directories inside Linux file system]]

You can go home using   *cd~* 

If you had to go to another user's home directory, use    *cd ~username*

To go back to last directory, use    *cd ~*

# Create Directories
To create directories in Linux, pass the name of directory as the argument to the   *mkdir*    command
For example:   ``$mkdir projects``       which will create directory named "projects". 

To create a directory within another directory use the -p flag. 
``$mkdir -p projects/linux/fundamentals``
The command creates the "fundamentals" directory within "linux" directory within the parent directory "projects".

# Copying Directories
In order to copy directories, you must include the option    **-r**    to the command which stands for "recursive" as it copies the directories and its contents. This option is necessary for directories regardless of an empty directory.

To copy a directory with its contents to the Public/docs/ path, run the command: 
``$cp -r projects Public/docs/


# Removing Directories
The     *rmdir*     command deletes an empty directory. If you try to remove a non-empty directory, you will get an error.



#linux 