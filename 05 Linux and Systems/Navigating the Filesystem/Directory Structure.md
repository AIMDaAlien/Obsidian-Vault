---
tags: [cli, linux]
created: 2025-09-15
publish: true
---
On windows, the *top level*  of the directory structure is called *My Computer*. Physical devices, such as hard drives or network drives, show up under My computer and are each assigned a drive letter such as C: or D:

A visual representation of a Windows directory structure:
<!-- embed removed: Pasted image 20230617124525.png (file not in vault) -->

Like Windows, the Linux directory structure, typically called a *filesystem*, also has a top level. However, My Computer is actually [[root directory]], sybolized as a slash /.
Theres also no drives in Linux; each physical drive is accessible under a directory rather than a drive letter.

<!-- embed removed: Pasted image 20230617124915.png (file not in vault) -->
Typical Linux filesystem

To view root contents, use `ls` with /
<!-- embed removed: Pasted image 20230617125009.png (file not in vault) -->

