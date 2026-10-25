---
tags: [cli, linux]
created: 2025-09-15
updated: 2026-10-25
publish: true
---
> Merged 2026-10-25 from: Absolute Paths, Relative Paths, Absolute vs. Relative pathnames.

The argument to `cd` is actually a path. A path is a list of directories separated by /.

<!-- embed removed: Pasted image 20230617214135.png (file not in vault) -->

There are two types of paths: [[Paths#Absolute Paths|Absolute Paths]] and [[Paths#Relative Paths|Relative Paths]]

## Absolute Paths

Allow the user to specify the exact location of a directory. Always starting at the root directory thus begins with /.
The path /home/sysadmin is an absolute path; tells the system to begin at the root, move into `home`, then into the `sysadmin` directory.

<!-- embed removed: Pasted image 20230617214633.png (file not in vault) -->
No output means the command succeeded. Go look in  [[pwd]].

## Relative Paths

Relative paths start from the current directory. It gives directions to a file to the current directory in the filesystem. They don't start with / but rather with the name of the directory contained within the current directory.

The argument is an example of the simplest relative path
<!-- embed removed: Pasted image 20230617215000.png (file not in vault) -->

If the user is located in the `Documents` directory, moving to the `Art` directory can be accomplished in a few ways.

<!-- embed removed: Pasted image 20230617215100.png (file not in vault) -->

Using the [[Paths#Absolute Paths|Absolute Paths]]:
<!-- embed removed: Pasted image 20230617215146.png (file not in vault) -->

Or multiple relative paths:
<!-- embed removed: Pasted image 20230617215208.png (file not in vault) -->

But simplest would be to use a single relative path that covers the origin to the destination directory.:
<!-- embed removed: Pasted image 20230617215259.png (file not in vault) -->
<!-- embed removed: Pasted image 20230619045956.png (file not in vault) -->

Use [[pwd]] to confirm you are in the path.

## Absolute vs. Relative pathnames

Suppose you are in the `/usr/share/doc` directory and you want to go to the `/usr/share/doc/bash` directory. Typing the command `cd /usr/share/doc/bash` results in a fair amount of typing. In cases like this, you want to use [[Paths#Relative Paths|Relative Paths]].

<!-- embed removed: Pasted image 20230619055043.png (file not in vault) -->
**Note:**  If there wasn't a bash directory under the current directory, the cmd would fail.
