---
tags: []
created: 2025-09-15
publish: true
---
`ls -l` displays file sizes in bytes. For text files, a byte is 1 character. For smaller files, byte sizes are fine. However for larger files, its hard to comprehend how large the file is.

<!-- embed removed: Pasted image 20230619052546.png (file not in vault) -->
The file size is hard to determine in bytes.

A lot of times, its preferrable to show the file size in a more human radable size, like mb or gb.

Use `ls -lh` to see them.
<!-- embed removed: Pasted image 20230619052738.png (file not in vault) -->

**Important:** The `-h` option must be used with the `-l` option.
