---
tags: [linux]
created: 2025-09-15
publish: true
---
`whatis` or `man -f` shows what section a [[Man Pages]] is stored in. This cmd sometimes gives weird output like:
<!-- embed removed: Pasted image 20230610215827.png (file not in vault) -->
The example above is designed to demonstrate a scenario where two commands list directory contents. The output in the example terminal above may not match the output in the VM.

Based on this output, there are two `ls` cmds that list directory contents.
Reason: UNIX had two main variants, which resulted in some cmds being developed "in parallel" thus behaving differently on different variants of UNIX. Modern distros include cmds from both UNIX variants.

So when `ls` is typed, which cmd is executed?? [[Man Pages#Where Are These Commands Located|Where Are These Commands Located]]

