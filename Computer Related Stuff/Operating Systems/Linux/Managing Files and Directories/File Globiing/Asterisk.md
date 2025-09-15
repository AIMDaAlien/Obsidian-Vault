##### The * is used to represent zero or more of any char in a filename. 

For example, to display all of the files in the `/etc` directory that begin with the letter `t`:
![[Pasted image 20230621155845.png]]
The pattern t* matches any file in the /etc directory that starts with the char *t*  followed by zero or more chars. 

You can use * at any place within the filename pattern.
For example, the following matches any filename in the /etc directory that ends with .d: 
![[Pasted image 20230621181449.png]]

All of the files in the /etc directory that begin with the letter `r` and end with `.conf` are shown in the following:
![[Pasted image 20230621181542.png]]
