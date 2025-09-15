The [] chars are used to match a single char by representing a range of chars that are possible matches. 
For example, the `/etc/[gu]*` pattern matches any file that begins with either a `g` or `u` character and contains zero or more additional characters:
![[Pasted image 20230621184757.png]]

[] can also be used to represent a range of characters. 
For example, the `/etc/[a-d]*` pattern matches all files that begin with any letter between and including a and d:
![[Pasted image 20230621184905.png]]

The `/etc/*[0-9]*` pattern shows any file that contains at least one number:
![[Pasted image 20230621184949.png]]

The range is based on ASCII text table. 
**the ASCII table can be viewed by executing `ascii` cmd.**
