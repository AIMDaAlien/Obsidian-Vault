---
tags: []
created: 2025-09-15
publish: true
---
When `-d` is used with [[ls]] , it refers to the current directory, and not the contents within it. Without other options, its rather meaningless. Recall that the current directory is always referred to with [[The . Char]].

<!-- embed removed: Pasted image 20230619052949.png (file not in vault) -->

 In this case, `-l`  shows the details of the contents in /home/sysadmin directory:
<!-- embed removed: Pasted image 20230619053100.png (file not in vault) -->

With the `-d`, the directory itself is listed:
<!-- embed removed: Pasted image 20230619053203.png (file not in vault) -->
Note the single period at the end of the long listing. This indicates that the current directory is being listed, and not the contents.