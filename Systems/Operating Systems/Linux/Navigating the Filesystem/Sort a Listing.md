By default, `ls` sorts files alphabetically by file name. Sometimes it may be useful to sort fiels using different criteria.

To sort files by size, use `-S`
![[Pasted image 20230619053621.png]]
**Capital S**

Its much more useful when used with `-l` so the file sizes are visible. 
![[Pasted image 20230619053738.png]]

Itd also be helpful to use `-h` [[Human-Readable Sizes]]:
![[Pasted image 20230619053825.png]]

For more detailed modification time info, use `--full-time` option to show the complete timestamp (including hours, minutes, seconds). It will assume `-l` automatically.
![[Pasted image 20230619054029.png]]

You could also reverse sort by using `-r`. Can also be combined with other options.
![[Pasted image 20230619054124.png]]
