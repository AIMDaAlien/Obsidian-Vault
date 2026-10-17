---
tags: []
created: 2025-09-15
publish: true
---
To be able to see the name of the kernel youre using, type the following cmd:
`uname`

The output should look like:
<!-- embed removed: Pasted image 20230608101212.png (file not in vault) -->


You can change what output is produced by a cmd by using option after the name of the cmd.
In lnux, options can sometimes be also given by two hyphen chars followed by a word or hyphenated word, for example:     `-nodename`

Execute the `uname` cmd again twice, once with the option `-n` and again with the option `-nodename`. This will display the network node hostname, also found in the prompt.

`uname -n`
`uname --nodename`

Your output should be similar to:
<!-- embed removed: Pasted image 20230608101657.png (file not in vault) -->

