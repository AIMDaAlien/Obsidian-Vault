---
tags: [cli, linux]
created: 2025-09-15
publish: true
---
Relative paths start from the current directory. It gives directions to a file to the current directory in the filesystem. They don't start with / but rather with the name of the directory contained within the current directory.

The argument is an example of the simplest relative path
<!-- embed removed: Pasted image 20230617215000.png (file not in vault) -->

If the user is located in the `Documents` directory, moving to the `Art` directory can be accomplished in a few ways.

<!-- embed removed: Pasted image 20230617215100.png (file not in vault) -->

Using the [[Absolute Paths]]:
<!-- embed removed: Pasted image 20230617215146.png (file not in vault) -->

Or multiple relative paths:
<!-- embed removed: Pasted image 20230617215208.png (file not in vault) -->

But simplest would be to use a single relative path that covers the origin to the destination directory.:
<!-- embed removed: Pasted image 20230617215259.png (file not in vault) -->
<!-- embed removed: Pasted image 20230619045956.png (file not in vault) -->

Use [[pwd]] to confirm you are in the path.
