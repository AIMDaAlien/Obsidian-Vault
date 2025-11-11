The ? Char represents any single char. Each question mark char matches exactly one char, no more or less. 

Suppose you want to show all of the files in the `/etc` directory that begin with the letter t and have exactly 7 chars after the t char. 
![[Pasted image 20230621184112.png]]

Glob chars can be used together to find even more complex patterns. The pattern `/etc/*????????????????????` command only matches files in the `/etc` directory with twenty or more chars in the filename:
![[Pasted image 20230621184157.png]]

The asterisk and question mark could also be used together to look for files with three-letter extensions by using `/etc/*.???` pattern:
![[Pasted image 20230621184540.png]]
