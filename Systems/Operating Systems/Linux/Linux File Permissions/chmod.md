##### To add read, write, and execute to the user of a particular file, we would type:
`chmod u+rwx file.txt`

##### On the other hand, the following cmd will take away read and write perms of that file for the group.
`chmod g-rw file.txt`


Its easy to get confused about the different perms and exactly how the system works. There is a simpler and faster way; just use numbers.

When you replace perms letters with numbers, you can calculate the required perms settings and input them into the system directly. We are aware of the three different perms, r w x , each perm is assigned to number as follows:
![[Pasted image 20230604162520.png]]

To correctly assign perms, you need to add up the level you want. If you want someone to get read and write, you 4 + 2 = 6 , or want someone to only be able to execute, it's 1. 0 means no perms 
![[Pasted image 20230604164749.png]]

If you want to give read, write, and execute to the owner and nothing to everyone else you get the number 700. (first digit is perms for the owner, second digit for the group, third for everyone else.) 
![[Pasted image 20230604181852.png]]

If you want to give full access to owner, read and execute to group, and execute to everyone else, you'd end up with 751
`$ chmod 751 file.txt`

777 would be anyone can do anything 




#linux 