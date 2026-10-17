---
tags: [cli, linux]
created: 2025-09-15
publish: true
---
[[ls]] is powerful in that it can help you navigate in the filesystem.

It can be used to list directory contents as well. Give the path to the directory as an argument. <!-- embed removed: Pasted image 20230619050809.png (file not in vault) -->

##### Consider This

On many Linux distributions, including the one used in our virtual machines, the `ls` command uses color to distinguish by file type. For example, directories may be displayed in blue, executable files may be displayed in green, and symbolic links may be displayed in cyan.

Colored output is not shown by default but rather the effect of the `--color` option. `ls` is performing the coloring automatically because theres an alias for ls cmd, so it runs with the --color option.
<!-- embed removed: Pasted image 20230619051017.png (file not in vault) -->

To avoid using the alias, use a `\` in front of your command: <!-- embed removed: Pasted image 20230619051055.png (file not in vault) -->

[[Listing Hidden Files]]

