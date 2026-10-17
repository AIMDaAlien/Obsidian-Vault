---
tags: []
created: 2025-09-15
publish: true
---
By default, `ls` sorts files alphabetically by file name. Sometimes it may be useful to sort fiels using different criteria.

To sort files by size, use `-S`
<!-- embed removed: Pasted image 20230619053621.png (file not in vault) -->
**Capital S**

Its much more useful when used with `-l` so the file sizes are visible.
<!-- embed removed: Pasted image 20230619053738.png (file not in vault) -->

Itd also be helpful to use `-h` [[Human-Readable Sizes]]:
<!-- embed removed: Pasted image 20230619053825.png (file not in vault) -->

For more detailed modification time info, use `--full-time` option to show the complete timestamp (including hours, minutes, seconds). It will assume `-l` automatically.
<!-- embed removed: Pasted image 20230619054029.png (file not in vault) -->

You could also reverse sort by using `-r`. Can also be combined with other options.
<!-- embed removed: Pasted image 20230619054124.png (file not in vault) -->
