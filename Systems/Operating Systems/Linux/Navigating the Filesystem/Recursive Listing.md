There's times where you want to show all of the files a directory as well as all of the files in all subdirectories under that directory. This is called *Recursive listing*.

Use `ls -R`
![[Pasted image 20230619053348.png]]

Note the files in `/etc/ppp` directory were listed first. Then came the contents of its subdirectories.

**Be careful with this option; for example, running the command on the root directory would list every file on the file system, including all files on any attached USB device and DVD in the system. Limit the use of recursive listings to smaller directory structures.**
